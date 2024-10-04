import unittest

from htmlnode import LeafNode, ParentNode
from block_markdown import markdown_to_blocks, block_to_block_type, BlockType, markdown_to_htmlnode

class TestMarkdownToBlocks(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(markdown_to_blocks(""), [])
                         
    def test_no_whitespaces_no_empty(self):
        markdown = "# heading\n\nparagraph\n\n* 1st item\n* 2nd item"
        self.assertEqual(markdown_to_blocks(markdown), ["# heading", "paragraph", "* 1st item\n* 2nd item"])

    def test_whitespaces_no_empty(self):
        markdown = "# heading  \n\n  paragraph"
        self.assertEqual(markdown_to_blocks(markdown), ["# heading", "paragraph"])

    def test_whitespaces_and_empty(self):
        markdown = "# heading  \n\n  \n\n paragraph"
        self.assertEqual(markdown_to_blocks(markdown), ["# heading","" , "paragraph"])


class TestBlockToBlockType(unittest.TestCase):
    def test_heading_1_hashtag(self):
        block = "# heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
    
    def test_heading_6_hashtags(self):
        block = "###### heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
    
    def test_heading_paragraph(self):
        block = "####### heading"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_code(self):
        block = "``` code block ```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
    
    def test_code_missing_end(self):
        block = "``` code block"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_quote(self):
        block = "> q1\n> q2\n> q3"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
    
    def test_quote_missing(self):
        block = "> q1\nq2\n> q3"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_unordered_list_asterisk(self):
        block = "* 1\n* 2\n* 3"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
    
    def test_unordered_list_dash(self):
        block = "- 1\n- 2\n- 3"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_unordered_list_missing_space(self):
        block = "- 1\n-2\n- 3"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list(self):
        block = "1. 1\n2. 2\n3. 3\n4. 4\n5. 5\n6. 6\n7. 7\n8. 8\n9. 9\n10. 10"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
    
    def test_ordered_list_missing(self):
        block = "1. 1\n2. 2\n3. 3\n5. 4\n5. 5\n6. 6\n7. 7\n8. 8\n9. 9\n10. 10"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_heading_hashtag(self):
        markdown = "# heading"
        self.assertEqual(markdown_to_htmlnode(markdown).to_html(),
                         "<div><h1>heading</h1></div>"
                         )
    
    def test_paragraph(self):
        markdown = "paragraph"
        self.assertEqual(markdown_to_htmlnode(markdown).to_html(),
                         "<div><p>paragraph</p></div>"
                         )

    def test_code(self):
        markdown = "``` code block ```"
        self.assertEqual(markdown_to_htmlnode(markdown).to_html(),
                         "<div><pre><code>code block </code></pre></div>"
                         )
    
    def test_quote(self):
        markdown = "> q1\n> q2\n> q3"
        self.assertEqual(markdown_to_htmlnode(markdown).to_html(),
                         "<div><blockquote>q1 q2 q3</blockquote></div>"
                         )
    
    def test_unordered_list(self):
        markdown = "* 1\n* 2\n* 3"
        self.assertEqual(markdown_to_htmlnode(markdown).to_html(),
                         "<div><ul><li>1</li><li>2</li><li>3</li></ul></div>"
                         )
        
    def test_ordered_list(self):
        markdown = "1. 1\n2. 2\n3. 3\n4. 4\n5. 5\n6. 6\n7. 7\n8. 8\n9. 9\n10. 10"
        self.assertEqual(markdown_to_htmlnode(markdown).to_html(),
                         "<div><ol><li>1</li><li>2</li><li>3</li><li>4</li><li>5</li><li>6</li><li>7</li><li>8</li><li>9</li><li>10</li></ol></div>"
                         )
        
    def test_mixed(self):
        markdown = '''
- ul1
- ul2 **bold text**

1. ol1 `code text`
2. ol2

paragraph *italic text*

'''
        self.assertEqual(markdown_to_htmlnode(markdown).to_html(),
                        "<div><ul><li>ul1</li><li>ul2 <b>bold text</b></li></ul><ol><li>ol1 <code>code text</code></li><li>ol2</li></ol><p>paragraph <i>italic text</i></p></div>"
                        )

if __name__ == "__main__":
    unittest.main()