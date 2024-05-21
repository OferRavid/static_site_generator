from textnode import (
    TextNode,
    text_node_to_html_node,
    text_type_code,
)

from htmlnode import ParentNode

from inline_markdown import text_to_textnodes

block_type_p = "paragraph"
block_type_h = "heading"
block_type_c = "code"
block_type_q = "quote"
block_type_ul = "unordered_list"
block_type_ol = "ordered_list"

heading_starts = ["#" * (i + 1) for i in range(6)]

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    final_blocks = []
    for block in blocks:
        if block == "":
            continue
        final_blocks.append(block.strip())
    return final_blocks

def block_to_block_type(block):
    lines = block.split("\n")
    if block.split(" ")[0] in heading_starts:
        return block_type_h
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return block_type_c
    if lines[0].startswith(">"):
        for line in lines[1:]:
            if not line.startswith(">"):
                return block_type_p
        return block_type_q
    if lines[0].startswith("* "):
        for line in lines[1:]:
            if not line.startswith("* "):
                return block_type_p
        return block_type_ul
    if lines[0].startswith("- "):
        for line in lines[1:]:
            if not line.startswith("- "):
                return block_type_p
        return block_type_ul
    if lines[0].startswith("1. "):
        i = 2
        for line in lines[1:]:
            if not line.startswith(f"{i}. "):
                return block_type_p
            i += 1
        return block_type_ol
    return block_type_p

def get_children(text):
    nodes = text_to_textnodes(text)
    children = []
    for node in nodes:
        html_node = text_node_to_html_node(node)
        children.append(html_node)
    return children

def code_block_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("Invalid code block")
    code = block.strip("```").strip()
    children = get_children(code)
    return ParentNode("pre", children)

def quote_block_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("Invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    quote = " ".join(new_lines)
    children = get_children(quote)
    return ParentNode("blockquote", children)

def list_block_to_list_items(block:str):
    if block_to_block_type(block) != block_type_ol and block_to_block_type(block) != block_type_ul:
        raise ValueError("Invalid list block")
    list_items = []
    lines = block.split("\n")
    for line in lines:
        item_sections = line.split(" ", 1)
        if len(item_sections) != 2 or item_sections[1] == "":
            raise ValueError("Invalid list block")
        children = get_children(item_sections[1])
        list_items.append(ParentNode("li", children))
    return list_items

def heading_block_to_html_node(block):
    heading_sections = block.split(" ", 1)
    if len(heading_sections) != 2:
        raise SyntaxError("Invalid syntax for heading")
    heading = heading_sections[0]
    if heading not in heading_starts:
        raise SyntaxError("Wrong syntax for markdown heading")
    level = len(heading)
    text = heading_sections[1]
    if text == "":
        raise ValueError("Invalid heading structure")
    children = get_children(text)
    return ParentNode(f"h{level}", children)

def paragraph_block_to_html_node(block):
    paragraph = " ".join(block.split("\n"))
    if paragraph == "":
        raise ValueError("Invalid paragraph block")
    nodes = text_to_textnodes(paragraph)
    return ParentNode("p", [text_node_to_html_node(node) for node in nodes])

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == block_type_c:
            html_children.append(code_block_to_html_node(block))
        elif block_type == block_type_q:
            html_children.append(quote_block_to_html_node(block))
        elif block_type == block_type_h:
            html_children.append(heading_block_to_html_node(block))
        elif block_type == block_type_p:
            html_children.append(paragraph_block_to_html_node(block))
        elif block_type == block_type_ol:
            html_children.append(ParentNode("ol", list_block_to_list_items(block)))
        else:
            html_children.append(ParentNode("ul", list_block_to_list_items(block)))
    return ParentNode("div", html_children)

