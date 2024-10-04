import re

from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue
        
        splitted_text = node.text.split(delimiter)

        if len(splitted_text) % 2 == 0:
            raise Exception("A matching closing delimiter is not found")

        flag = 1
        for text in splitted_text:
            flag = (flag + 1) % 2
            if text == "":
                continue

            if flag:
                new_nodes.append(TextNode(text, text_type))
            else:
                new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        for alt, link in extract_markdown_images(text):
            splitted_text = text.split(f"![{alt}]({link})", 1)
            if splitted_text[0] != "":
                new_nodes.append(TextNode(splitted_text[0], node.text_type))
            new_nodes.append(TextNode(alt, TextType.IMAGE, link))
            text = splitted_text[-1]

        if text:
            new_nodes.append(TextNode(text, node.text_type))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        for alt, link in extract_markdown_links(text):
            splitted_text = text.split(f"[{alt}]({link})", 1)
            if splitted_text[0] != "":
                new_nodes.append(TextNode(splitted_text[0], node.text_type))
            new_nodes.append(TextNode(alt, TextType.LINK, link))
            text = splitted_text[-1]
        
        if text:
            new_nodes.append(TextNode(text, node.text_type))
    return new_nodes

def text_to_textnodes(text):
    DELIMITERS = {TextType.BOLD: "**", TextType.ITALIC: "*", TextType.CODE: "`"}
    
    splitted_text = [TextNode(text, TextType.TEXT)]

    for text_type, delimiter in DELIMITERS.items():
        splitted_text = split_nodes_delimiter(splitted_text, delimiter, text_type)
    
    splitted_text = split_nodes_image(splitted_text)
    splitted_text = split_nodes_link(splitted_text)

    return splitted_text