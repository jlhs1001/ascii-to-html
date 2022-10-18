import bisect

color_lookup = {
    1: "font-weight:bold",
    4: "text-decoration:underline",
    9: "text-decoration:line-through",
    30: "color:#000000",
    31: "color:#CD0000",
    32: "color:#00CD00",
    33: "color:#CDCD00",
    34: "color:#0000EE",
    35: "color:#CD00CD",
    36: "color:#00CDCD",
    37: "color:#E5E5E5",
    40: "background-color:#000000",
    41: "background-color:#CD0000",
    42: "background-color:#00CD00",
    43: "background-color:#CDCD00",
    44: "background-color:#0000EE",
    45: "background-color:#CD00CD",
    46: "background-color:#00CDCD",
    47: "background-color:#E5E5E5",
    90: "color:#7F7F7F",
    91: "color:#FF0000",
    92: "color:#00FF00",
    93: "color:#FFFF00",
    94: "color:#5C5CFF",
    95: "color:#FF00FF",
    96: "color:#00FFFF",
    97: "color:#FFFFFF",
    100: "background-color:#7F7F7F",
    101: "background-color:#FF0000",
    102: "background-color:#00FF00",
    103: "background-color:#FFFF00",
    104: "background-color:#5C5CFF",
    105: "background-color:#FF00FF",
    106: "background-color:#00FFFF",
    107: "background-color:#FFFFFF",
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

    def generate_tag(self, text_state):
        if self.inline_css:
            return f"<span style=\"" \
                   f"{color_lookup[text_state.background] if text_state.background != 0 else ''}" \
                   f"{';' + color_lookup[text_state.foreground] if text_state.foreground != 0 else ''}" \
                   f"{';' + color_lookup[1] if text_state.bold else ''}\">" \
                   f"{';' + color_lookup[4] if text_state.underlined else ''}" \
                   f"{';' + color_lookup[9] if text_state.underlined else ''}\">"
        else:
            return f"<span class=\"" \
                   f"{'ansi' + str(text_state.background) if text_state.background != 0 else ''}" \
                   f"{' ansi' + str(text_state.foreground) if text_state.foreground != 0 else ''}" \
                   f"{' ansi1' if text_state.bold else ''}\">" \
                   f"{' ansi4' if text_state.underlined else ''}" \
                   f"{' ansi9' if text_state.underlined else ''}\">"

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
        res = ".ansiDefault{color:#FFFFFF}.ansiBackground{background-color:#000000}"
        for code, color in color_lookup.items():
            res += f".ansi{code}{{{color}}}\n"
        return res

