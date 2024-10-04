import unittest

from markdown_to_html import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_1(self):
        markdown = """# title

paragraph
"""
        self.assertEqual(extract_title(markdown), "title")


if __name__ == "__main__":
    unittest.main()