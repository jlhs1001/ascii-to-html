import unittest
from src import ascii_to_html


test_data = {
    'underline': '<span></span><span class=" ansiUnderline">hello</span>',
    'underline_reset': '<span></span><span class=" ansiUnderline">hello </span><span class=" ">world</span>',
    'underline_reset_red': '<span></span><span class=" ansiUnderline">hello </span><span class=" ">world</span>',
}


class TestAnsiToHtmlOutput(unittest.TestCase):
    def test_underline(self):
        self.assertEqual(ascii_to_html('\x1b[4mhello', insert_nbsp=True), test_data['underline'])

    def test_underline_reset_red(self):
        self.assertEqual(ascii_to_html('\x1b[4mhello \x1b[0;32mworld'), test_data['underline_reset_red'])

    def test_underline_reset(self):
        self.assertEqual(ascii_to_html('\x1b[4mhello \x1b[0mworld'), test_data['underline_reset_red'])


if __name__ == '__main__':
    unittest.main()
