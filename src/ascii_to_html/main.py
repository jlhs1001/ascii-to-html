color_lookup = {
    1: "font-weight:bold",
    4: "text-decoration:underline",
    30: "color:rgb(0,0,0)",
    31: "color:rgb(205,0,0)",
    32: "color:rbg(0,205,0",
    33: "color:rgb(205,205,0)",
    34: "color:rgb(0,0,238)",
    35: "color:rgb(205,0,205)",
    36: "color:rgb(0,205,205)",
    37: "color:rgb(229,229,229)",
    40: "background-color:rgb(0,0,0)",
    41: "background-color:rgb(205,0,0)",
    42: "background-color:rbg(0,205,0",
    43: "background-color:rgb(205,205,0)",
    44: "background-color:rgb(0,0,238)",
    45: "background-color:rgb(205,0,205)",
    46: "background-color:rgb(0,205,205)",
    47: "background-color:rgb(229,229,229)",
    90: "color:rgb(127,127,127)",
    91: "color:rgb(255,0,0)",
    92: "color:rgb(0,255,0)",
    93: "color:rgb(255,255,0)",
    94: "color:rgb(92,92,255)",
    95: "color:rgb(255,0,255)",
    96: "color:rgb(0,255,255)",
    97: "color:rgb(255,255,255)",
    100: "background-color:rgb(127,127,127)",
    101: "background-color:rgb(255,0,0)",
    102: "background-color:rgb(0,255,0)",
    103: "background-color:rgb(255,255,0)",
    104: "background-color:rgb(92,92,255)",
    105: "background-color:rgb(255,0,255)",
    106: "background-color:rgb(0,255,255)",
    107: "background-color:rgb(255,255,255)",
}

CSS_TEMPLATE = f"""
.ansi_fore{{color: #FFFFFF}}
.ansi_back{{background-color:#000000}}
.ansi1{{font-weight:bold}}
.ansi4{{text-decoration: underline}}
.ansi9{{text-decoration: line-through}}
.ansi30{{color:rgb(0,0,0)}}
.ansi31{{color:rgb(205,0,0)}}
.ansi32{{color:rbg(0,205,0}}
.ansi33{{color:rgb(205,205,0)}}
.ansi34{{color:rgb(0,0,238)}}
.ansi35{{color:rgb(205,0,205)}}
.ansi36{{color:rgb(0,205,205)}}
.ansi37{{color:rgb(229,229,229)}}
.ansi40{{color:rgb(0,0,0)}}
.ansi41{{color:rgb(205,0,0)}}
.ansi42{{color:rbg(0,205,0}}
.ansi43{{color:rgb(205,205,0)}}
.ansi44{{color:rgb(0,0,238)}}
.ansi45{{color:rgb(205,0,205)}}
.ansi46{{color:rgb(0,205,205)}}
.ansi47{{color:rgb(229,229,229)}}
.ansi90{{color:rgb(127,127,127)}}
.ansi91{{color:rgb(255,0,0)}}
.ansi92{{color:rgb(0,255,0)}}
.ansi93{{color:rgb(255,255,0)}}
.ansi94{{color:rgb(92,92,255)}}
.ansi95{{color:rgb(255,0,255)}}
.ansi96{{color:rgb(0,255,255)}}
.ansi97{{color:rgb(255,255,255)}}
.ansi100{{background-color:rgb(127,127,127)}}
.ansi101{{background-color:rgb(255,0,0)}}
.ansi102{{background-color:rgb(0,255,0)}}
.ansi103{{background-color:rgb(255,255,0)}}
.ansi104{{background-color:rgb(92,92,255)}}
.ansi105{{background-color:rgb(255,0,255)}}
.ansi106{{background-color:rgb(0,255,255)}}
.ansi107{{background-color:rgb(255,255,255)}}
"""


# -- Some helper functions to tidy things up --


def is_background(code):
    return 30 <= code <= 37 or 90 <= code <= 97


def is_foreground(code):
    return 40 <= code <= 47 or 100 <= code <= 107


def is_bold(code):
    return code == 1


def is_underline(code):
    return code == 4


class TextEffectState:
    """ Keeps track of current text styling and effects """

    def __init__(self, background=0, foreground=0, underlined=False, bold=False):
        """
        :param background: Current background color
        :param foreground: Current foreground color
        :param underlined: Current underlined state
        :param bold: Current bold state
        """
        self.background = background
        self.foreground = foreground
        self.underlined = underlined
        self.bold = bold

    def update(self, codes):
        for code in codes:
            if code == 0:
                # reset code
                self.background = 0
                self.foreground = 0
                self.underlined = False
                self.bold = False
            elif is_background(code):
                self.background = code
            elif is_foreground(code):
                self.foreground = code
            elif is_underline(code):
                self.underlined = True
            elif is_bold(code):
                self.bold = True

    def __eq__(self, other):
        """

        :param other: Other TextEffectState to compare state with.
        :return: Whether equivalent or not
        """
        return (self.background != other.background or
                self.foreground != other.foreground or
                self.underlined != other.underlined or
                self.bold != other.bold)

    def props(self):
        return [self.background, self.foreground, self.underlined, self.bold]


class AsciiConverter:
    """ Convert ASCII to HTML efficiently, and with ease. """
    result = ""

    prev_effect_state = TextEffectState()
    text_effect_state = TextEffectState()

    def __init__(self, insert_nbsp=False, inline_css=False):
        """
        :param insert_nbsp: Replace spaces with non-breaking spaces
        :param inline_css: Whether to generate tags with inline css or classes
        """
        self.insert_nbsp = insert_nbsp
        self.inline_css = inline_css

    def to_html(self, source):
        result = ""

        result += "<span style=\"display: none\">"
        index = 0
        while index < len(source):
            if source[index] == "\x1b":
                # grab the sequence to 'm', which is
                # the (standardized) sequence end delimiter.
                numbers_str = source[index + 2:].split("m")[0]
                # then parse the codes into a sequence.
                sequence = AsciiConverter.parse_sequence(numbers_str)

                changes_state = False
                for code in sequence:
                    if code not in self.text_effect_state.props():
                        changes_state = True
                        break

                if changes_state:
                    # update text effect state
                    self.text_effect_state.update(sequence)

                    # close previous state and add new state
                    result += "</span>" + self.generate_tag(self.text_effect_state)

                index += len(numbers_str) + 3  # move past escape sequence
            else:
                index += 1
            try:
                if self.insert_nbsp and source[index] == " ":
                    result += "&nbsp;"
                elif source[index] == "\n":
                    result += "<br>"
                elif source[index] != "\x1b":
                    result += source[index]
            except IndexError:
                pass
        return result + "</span>"

    @staticmethod
    def parse_sequence(sequence):
        """ Parse ANSI escape sequence string into a list of numbers

        :param sequence: Sequence of codes to parse
        :return: List of codes
        """
        try:
            return [int(num) for num in sequence.split(";")]
        except ValueError:
            if "" in sequence.split(""):
                raise ValueError("Invalid character in escape sequence. Must be a number.\n\n\x1b[4;32m"
                                 "[Hint]\x1b[0m: Found a code with nothing!'")
            else:
                raise ValueError("Invalid character in escape sequence. Must be a number.")

    @staticmethod
    def generate_css():
        return CSS_TEMPLATE

    def generate_tag(self, text_state):
        if self.inline_css:
            return f"<span style=\"" \
                   f"{color_lookup[text_state.background] if text_state.background != 0 else ''}" \
                   f"{';' + color_lookup[text_state.foreground] if text_state.foreground != 0 else ''}" \
                   f"{';' + color_lookup[4] if text_state.underlined else ''}" \
                   f"{';' + color_lookup[1] if text_state.bold else ''}\">"
        else:
            return f"<span class=\"" \
                   f"{'ansi' + str(text_state.background) if text_state.background != 0 else ''}" \
                   f"{' ansi' + str(text_state.foreground) if text_state.foreground != 0 else ''}" \
                   f"{' ansiUnderlined' if text_state.underlined else ''}" \
                   f"{' ansiBold' if text_state.bold else ''}\">"

x = 47
for i in range(30, 38):
    print(f"\x1b[{x}m\x1b[{i}mascii_to_html")
    x -= 1
