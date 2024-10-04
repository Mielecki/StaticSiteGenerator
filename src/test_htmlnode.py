import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")
    
    def test_props_to_html_2(self):
        node = HTMLNode(props={"href": "https://google.com",
                               "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://google.com" target="_blank"')
    
    def test_repr(self):
        node = HTMLNode()
        self.assertEqual(repr(node), "HTMLNode(tag=None, value=None, children=None, props=None)")

class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        node = LeafNode("a", "abcde", {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com" target="_blank">abcde</a>')

    def test_to_html_2(self):
        node = LeafNode("p", "abcde")
        self.assertEqual(node.to_html(), '<p>abcde</p>')

class TestParentNode(unittest.TestCase):
    def test_to_html(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

    def test_to_html_2(self):
        node1 = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
            ],
        )
        node2 = ParentNode(
            "a",
            [
                node1,
                LeafNode("i", "italic text", {"class": "abcde"}),
            ],
            {
                "href": "https://www.google.com"
            }
        )
        self.assertEqual(node2.to_html(), '<a href="https://www.google.com"><p><b>Bold text</b>Normal text</p><i class="abcde">italic text</i></a>')

    def test_to_html_3(self):
        node1 = ParentNode(
            "p",
            [],
        )

        with self.assertRaises(ValueError) as e:
            node1.to_html()

        self.assertTrue('ParentNode must have children' in str(e.exception))


if __name__ == "__main__":
    unittest.main()