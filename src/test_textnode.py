import unittest

from textnode import TextNode, text_node_to_html
from htmlnode import LeafNode

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node1 = TextNode("Text", "bold")
        node2 = TextNode("Text", "bold")
        self.assertEqual(node1, node2)
    
    def test_eq_false(self):
        node1 = TextNode("Text", "bold")
        node2 = TextNode("TextText","bold")
        self.assertNotEqual(node1, node2)

    def test_eq_false2(self):
        node1 = TextNode("Text", "bold")
        node2 = TextNode("Text", "italic")
        self.assertNotEqual(node1, node2)

    def test_eq_none(self):
        node1 = TextNode("Text", "bold")
        node2 = TextNode("Text", "bold", None)
        self.assertEqual(node1, node2)

    def test_eq_url(self):
        node1 = TextNode("Text", "bold", "abc")
        node2 = TextNode("Text", "bold", "abc")
        self.assertEqual(node1, node2)

    def test_repr(self):
        node = TextNode("Text", "bold", "abc")
        self.assertEqual("TextNode(Text, bold, abc)", repr(node))


class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_type_text(self):
        node = text_node_to_html(TextNode("abcde", "text"))
        self.assertEqual(node.tag, None)
        self.assertEqual(node.value, "abcde")
        self.assertEqual(node.props, None)
    
    def test_type_bold(self):
        node = text_node_to_html(TextNode("abcde", "bold"))
        self.assertEqual(node.tag, "b")
        self.assertEqual(node.value, "abcde")
        self.assertEqual(node.props, None)
    
    def test_type_italic(self):
        node = text_node_to_html(TextNode("abcde", "italic"))
        self.assertEqual(node.tag, "i")
        self.assertEqual(node.value, "abcde")
        self.assertEqual(node.props, None)

    def test_type_code(self):
        node = text_node_to_html(TextNode("abcde", "code"))
        self.assertEqual(node.tag, "code")
        self.assertEqual(node.value, "abcde")
        self.assertEqual(node.props, None)

    def test_type_link(self):
        node = text_node_to_html(TextNode("abcde", "link", "google.com"))
        self.assertEqual(node.tag, "a")
        self.assertEqual(node.value, "abcde")
        self.assertEqual(node.props, {"href": "google.com"})
    
    def test_type_link(self):
        node = text_node_to_html(TextNode("abcde", "image", "google.com"))
        self.assertEqual(node.tag, "img")
        self.assertEqual(node.value, "")
        self.assertEqual(node.props, {"src": "google.com", "alt": "abcde"})


if __name__ == "__main__":
    unittest.main()