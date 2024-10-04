from enum import Enum

from htmlnode import ParentNode, LeafNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    output = markdown.split("\n\n")
    output = list(filter(lambda x: not x == "", output))
    output = list(map(lambda x: x.strip(), output))
    return output


def scan_lines(block, pattern):
    splitted_block = block.split("\n")
    for line in splitted_block:
        if len(line) < len(pattern) or line[:len(pattern)] != pattern:
            return False
    
    return True

def block_to_block_type(block):
    if block[0] == "#":
        space = block.find(" ")
        if space > 6:
            return BlockType.PARAGRAPH
        return BlockType.HEADING
    
    elif len(block) >= 6 and block[:3] == "```" and block[-3:] == "```":
        return BlockType.CODE
    
    elif block[0] == ">":
        return BlockType.QUOTE if scan_lines(block, ">") else BlockType.PARAGRAPH
    
    elif block[:2] in ["* ", "- "]:
        return BlockType.UNORDERED_LIST if scan_lines(block, "* ") or scan_lines(block, "- ") else BlockType.PARAGRAPH
    
    elif block[:3] == "1. ":
        splitted_block = block.split("\n")
        i = 1
        for line in splitted_block:
            if len(line) < len(str(i)) + 2 or line[:len(str(i)) + 2] != f"{i}. ":
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH

def text_to_htmlnodes(text):
    text_nodes = text_to_textnodes(text)
    nodes = []

    for text_node in text_nodes:
        node = text_node_to_html(text_node)
        nodes.append(node)

    return nodes
        

def block_to_heading_htmlnode(block):
    text = block.lstrip("#")[1:]
    heading_number = len(block) - len(text) - 1

    node = ParentNode(f"h{heading_number}", text_to_htmlnodes(text))
    return node

def block_to_paragraph_htmlnode(block):
    lines = block.split('\n')
    text = " ".join(lines)
    node = ParentNode("p", text_to_htmlnodes(text))

    return node

def block_to_quote_htmlnode(block):
    lines = block.split('\n')
    new_lines = []
    for line in lines:
        new_lines.append(line[2:])
    text = " ".join(new_lines)
    node = ParentNode("blockquote", text_to_htmlnodes(text))

    return node

def block_to_code_htmlnode(block):
    text = block[4:-3]
    nested_node = ParentNode("code", text_to_htmlnodes(text))
    node = ParentNode("pre", [nested_node])

    return node

def block_to_ordered_list_htmlnode(block):
    blocks = block.split('\n')
    children = []

    for i, block in enumerate(blocks):
        text = block[3 + (len(str(i+1))-1):]
        children.append(ParentNode("li", text_to_htmlnodes(text)))

    node = ParentNode("ol", children)

    return node

def block_to_unordered_list_htmlnode(block):
    blocks = block.split('\n')
    children = []

    for i, block in enumerate(blocks):
        text = block[2:]
        children.append(ParentNode("li", text_to_htmlnodes(text)))

    node = ParentNode("ul", children)

    return node

def block_to_htmlnode(block):
    block_type = block_to_block_type(block)

    match block_type:
        case BlockType.HEADING:
            return block_to_heading_htmlnode(block)
        case BlockType.PARAGRAPH:
            return block_to_paragraph_htmlnode(block)
        case BlockType.QUOTE:
            return block_to_quote_htmlnode(block)
        case BlockType.CODE:
            return block_to_code_htmlnode(block)
        case BlockType.ORDERED_LIST:
            return block_to_ordered_list_htmlnode(block)
        case BlockType.UNORDERED_LIST:
            return block_to_unordered_list_htmlnode(block)
        case _:
            raise ValueError(f"Invalid block type: {block_type}")

def markdown_to_htmlnode(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []

    for block in blocks:
        children.append(block_to_htmlnode(block))

    return ParentNode("div", children)