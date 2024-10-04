import unittest

from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes
from textnode import TextNode, TextType

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_non_text_only(self):
        node1 = TextNode("bold", TextType.BOLD)
        node2 = TextNode("italic", TextType.ITALIC)
        self.assertEqual(split_nodes_delimiter([node1, node2], '`', TextType.CODE), [node1, node2])

    def test_text_only(self):
        node = TextNode("normal text **bold text** normal text", TextType.TEXT)
        self.assertEqual(
            split_nodes_delimiter([node], "**", TextType.BOLD),
            [
                TextNode("normal text ", TextType.TEXT),
                TextNode("bold text", TextType.BOLD),
                TextNode(" normal text", TextType.TEXT),
            ]
        )
    
    def test_mixed(self):
        node1 = TextNode("bold", TextType.BOLD)
        node2 = TextNode("normal text **bold text** normal text", TextType.TEXT)
        self.assertEqual(
            split_nodes_delimiter([node1, node2], "**", TextType.BOLD),
            [
                node1,
                TextNode("normal text ", TextType.TEXT),
                TextNode("bold text", TextType.BOLD),
                TextNode(" normal text", TextType.TEXT),
            ]
        )
    
    def test_non_closing(self):
        node = TextNode("normal text **bold text normal text", TextType.TEXT)
        with self.assertRaises(Exception) as e:
            split_nodes_delimiter([node], "**", TextType.BOLD)
        
        self.assertTrue("A matching closing delimiter is not found" in str(e.exception))
    
    def test_non_matching(self):
        node = TextNode("normal text **bold text** normal text", TextType.TEXT)
        self.assertEqual(split_nodes_delimiter([node], '`', TextType.CODE), [node])

    def test_starting_with_delimiter(self):
        node = TextNode("**bold text** normal text", TextType.TEXT)
        self.assertEqual(split_nodes_delimiter([node], '**', TextType.BOLD),
                         [
                            TextNode("bold text", TextType.BOLD),
                            TextNode(" normal text", TextType.TEXT),
                         ],
                         )
    
    def test_next_to_each_other(self):
        node = TextNode("**bold text****bold text**", TextType.TEXT)
        self.assertEqual(split_nodes_delimiter([node], '**', TextType.BOLD),
                         [
                            TextNode("bold text", TextType.BOLD),
                            TextNode("bold text", TextType.BOLD),
                         ],
                         )

class TestExtractMarkdownImages(unittest.TestCase):
    def test_single_matching_image(self):
        text = "text ![image](https://li.nk/image.img) text"
        self.assertEqual(extract_markdown_images(text), [("image", "https://li.nk/image.img")])

    def test_multiple_matching_images(self):
        text = "text ![image1](https://li.nk/image1.img)![image2](https://li.nk/image2.img) text![image3](https://li.nk/image3.img)"
        self.assertEqual(extract_markdown_images(text), [("image1", "https://li.nk/image1.img"),
                                                         ("image2", "https://li.nk/image2.img"),
                                                         ("image3", "https://li.nk/image3.img"),
                                                         ]
                                                         )

class TestExtractMarkdownLinks(unittest.TestCase):
    def test_single_matching_link(self):
        text = "text [link](https://google.com) text"
        self.assertEqual(extract_markdown_links(text), [("link", "https://google.com")])

    def test_mulitple_matching_links(self):
        text = "text [link1](https://google.com)[link2](https://google.com) text[link3](https://google.com)"
        self.assertEqual(extract_markdown_links(text), [("link1", "https://google.com"),
                                                        ("link2", "https://google.com"),
                                                        ("link3", "https://google.com")
                                                        ])
    def test_non_matching_image(self):
        text = "text ![image](https://li.nk/image.img) text"
        self.assertEqual(extract_markdown_links(text), [])


class TestSplitNodesImage(unittest.TestCase):
    def test_single_matching_image(self):
        node = TextNode("text ![image](https://li.nk/image.img) text", TextType.TEXT)
        self.assertEqual(split_nodes_image([node]), [
            TextNode("text ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, 'https://li.nk/image.img'),
            TextNode(" text", TextType.TEXT),
        ])
    
    def test_multiple_matching_images(self):
        node = TextNode("text ![image1](https://li.nk/image.img)![image2](https://li.nk/image.img) text![image3](https://li.nk/image.img)", TextType.TEXT)
        self.assertEqual(split_nodes_image([node]), [
            TextNode("text ", TextType.TEXT),
            TextNode("image1", TextType.IMAGE, 'https://li.nk/image.img'),
            TextNode("image2", TextType.IMAGE, 'https://li.nk/image.img'),
            TextNode(" text", TextType.TEXT),
            TextNode("image3", TextType.IMAGE, 'https://li.nk/image.img'),
        ])

    def test_multiple_nodes(self):
        node1 = TextNode("text ![image1](https://li.nk/image.img)![image2](https://li.nk/image.img) text![image3](https://li.nk/image.img)", TextType.TEXT)
        node2 = TextNode("![image4](https://li.nk/image.img)![image5](https://li.nk/image.img) text![image6](https://li.nk/image.img)", TextType.TEXT)
        node3 = TextNode("non maching", TextType.TEXT)
        self.assertEqual(split_nodes_image([node1, node2, node3]), [
            TextNode("text ", TextType.TEXT),
            TextNode("image1", TextType.IMAGE, 'https://li.nk/image.img'),
            TextNode("image2", TextType.IMAGE, 'https://li.nk/image.img'),
            TextNode(" text", TextType.TEXT),
            TextNode("image3", TextType.IMAGE, 'https://li.nk/image.img'),
            TextNode("image4", TextType.IMAGE, 'https://li.nk/image.img'),
            TextNode("image5", TextType.IMAGE, 'https://li.nk/image.img'),
            TextNode(" text", TextType.TEXT),
            TextNode("image6", TextType.IMAGE, 'https://li.nk/image.img'),
            TextNode("non maching", TextType.TEXT),
        ])

class TestSplitNodesLink(unittest.TestCase):
    def test_single_matching_link(self):
        node = TextNode("text [image](https://li.nk/image) text", TextType.TEXT)
        self.assertEqual(split_nodes_link([node]), [
            TextNode("text ", TextType.TEXT),
            TextNode("image", TextType.LINK, 'https://li.nk/image'),
            TextNode(" text", TextType.TEXT),
        ])
    
    def test_multiple_matching_links(self):
        node = TextNode("text [image1](https://li.nk/image)[image2](https://li.nk/image) text[image3](https://li.nk/image)", TextType.TEXT)
        self.assertEqual(split_nodes_link([node]), [
            TextNode("text ", TextType.TEXT),
            TextNode("image1", TextType.LINK, 'https://li.nk/image'),
            TextNode("image2", TextType.LINK, 'https://li.nk/image'),
            TextNode(" text", TextType.TEXT),
            TextNode("image3", TextType.LINK, 'https://li.nk/image'),
        ])

    def test_multiple_nodes(self):
        node1 = TextNode("text [image1](https://li.nk/image)[image2](https://li.nk/image) text[image3](https://li.nk/image)", TextType.TEXT)
        node2 = TextNode("[image4](https://li.nk/image)[image5](https://li.nk/image) text[image6](https://li.nk/image)", TextType.TEXT)
        node3 = TextNode("non maching", TextType.TEXT)
        self.assertEqual(split_nodes_link([node1, node2, node3]), [
            TextNode("text ", TextType.TEXT),
            TextNode("image1", TextType.LINK, 'https://li.nk/image'),
            TextNode("image2", TextType.LINK, 'https://li.nk/image'),
            TextNode(" text", TextType.TEXT),
            TextNode("image3", TextType.LINK, 'https://li.nk/image'),
            TextNode("image4", TextType.LINK, 'https://li.nk/image'),
            TextNode("image5", TextType.LINK, 'https://li.nk/image'),
            TextNode(" text", TextType.TEXT),
            TextNode("image6", TextType.LINK, 'https://li.nk/image'),
            TextNode("non maching", TextType.TEXT),
        ])

    def test_image(self):
        node = TextNode("image", TextType.IMAGE, "https://image.com/image.img")
        self.assertEqual(split_nodes_link([node]), [node])


class TestTextToTextnodes(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(text_to_textnodes(""), [])

    def test_1(self):
        text = 'normal text **bold text **[link](https://www.li.nk) *italic text* ![image](https://www.ima.ge/image.img) `code text`'
        self.assertEqual(text_to_textnodes(text),
                         [
                             TextNode("normal text ", TextType.TEXT),
                             TextNode("bold text ", TextType.BOLD),
                             TextNode("link", TextType.LINK, "https://www.li.nk"),
                             TextNode(" ", TextType.TEXT),
                             TextNode("italic text", TextType.ITALIC),
                             TextNode(" ", TextType.TEXT),
                             TextNode("image", TextType.IMAGE, "https://www.ima.ge/image.img"),
                             TextNode(" ", TextType.TEXT),
                             TextNode("code text", TextType.CODE)
                         ])
                         

if __name__ == "__main__":
    unittest.main()