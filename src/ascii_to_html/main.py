import bisect

color_lookup = {
    1: "font-weight:bold",
    4: "text-decoration:underline",
    9: "text-decoration:line-through",
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

# -- Some helper functions to tidy things up --


def is_background(code): return 30 <= code <= 37 or 90 <= code <= 97
def is_foreground(code): return 40 <= code <= 47 or 100 <= code <= 107
def is_strikethrough(code): return code == 9
def is_underline(code): return code == 4
def is_bold(code): return code == 1


class TextEffectState:
    """ Keeps track of current text styling and effects """

    def __init__(self):
        self.background = 0
        self.foreground = 0
        self.underlined = False
        self.bold = False
        self.strikethrough = False

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
            elif is_strikethrough(code):
                self.strikethrough = True

    def __iter__(self):
        """ Allow iteration through properties

        :return: iterable list of properties
        """
        return iter([self.background, self.foreground, self.underlined, self.bold])


class AsciiConverter:
    """ Convert ASCII to HTML efficiently, and with ease. """

    def __init__(self, insert_nbsp=True, inline_css=True, verbose=False):
        """
        :param insert_nbsp: Replace spaces with non-breaking spaces
        :param inline_css: Whether to generate tags with inline css or classes
        :param verbose: Include verbose logging such as: "Invalid tag found: x"
        """
        self.insert_nbsp = insert_nbsp
        self.inline_css = inline_css
        self.verbose = verbose

        self.text_effect_state = TextEffectState()

    def to_html(self, source):
        has_found_escape = False
        result = '<span class="ansiDefault ansiBackground">'
        index = 0
        while index < len(source):
            if source[index] == "\x1b":
                # grab the sequence to 'm', which is
                # the (standardized) sequence delimiter.
                numbers_str = source[index + 2:].split("m")[0]
                # then parse the codes into a sequence.
                sequence = AsciiConverter.parse_sequence(numbers_str)

                changes_state = False
                for code in sequence:
                    if code not in self.text_effect_state:
                        changes_state = True
                        break

                if changes_state:
                    # update text effect state
                    self.text_effect_state.update(sequence)

                    if self.verbose:
                        for code in sequence:
                            if code not in color_lookup.keys():
                                print(f"\x1b[1;33m[WARNING]:\x1b[0m Found invalid code: {code}")

                    # close previous state and add new state
                    result += ("</span>" if has_found_escape else "") + self.generate_tag(self.text_effect_state)
                    has_found_escape = True
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
        # close out final span and parent span
        return result + "</span></span>"

    @staticmethod
    def parse_sequence(sequence):
        """ Parse ANSI escape sequence string into a list of numbers

        :param sequence: Sequence of codes to parse
        :return: List of codes
        """
        try:
            return [int(num) for num in sequence.split(";")]
        except ValueError:
            # Must be a number, so handle an instance where
            # end-developer mistakenly uses something else:
            if "" in sequence.split(""):
                raise ValueError("Invalid character in escape sequence. Must be a number.\n\n\x1b[4;32m"
                                 "[Hint]\x1b[0m: Found a code with nothing!'")
            else:
                raise ValueError("Invalid character in escape sequence. Must be a number.")

    @staticmethod
    def generate_css():
        res = ".ansiDefault{#FFFFFF}.ansiBackground{#000000}"
        for code, color in color_lookup.items():
            res += f".ansi{code}{{{color}}}\n"
        return res

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
