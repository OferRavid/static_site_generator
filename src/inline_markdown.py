import re

from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_link,
    text_type_image,
)

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    if not old_nodes:
        return []
    new_nodes = []
    for node in old_nodes:
        if node.text.count(delimiter) % 2 == 1:
            raise SyntaxError(f"Invalid syntax for markdown text: missing closing {delimiter}.")
        if node.text_type != text_type_text or delimiter not in node.text:
            new_nodes.append(node)
            continue
        new_text = node.text.split(delimiter)
        for i in range(len(new_text)):
            text = new_text[i]
            if len(text) == 0:
                continue
            cur_type = node.text_type
            if i % 2 == 1:
                cur_type = text_type
            new_node = TextNode(text, cur_type)
            new_nodes.append(new_node)
    return new_nodes

def extract_markdown_images(text):
    regex = r"!\[(.*?)\]\((.*?)\)"
    matches = re.findall(regex, text)
    return matches

def extract_markdown_links(text):
    regex = r"\[(.*?)\]\((.*?)\)"
    matches = re.findall(regex, text)
    return matches

def split_nodes_helper(old_nodes, text_type, func):
    if not old_nodes:
        return []
    exclamation_point = "!"
    if text_type == text_type_link:
        exclamation_point = ""
    new_nodes = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue
        old_text = node.text
        images_or_links = func(old_text)
        if len(images_or_links) == 0:
            new_nodes.append(node)
            continue
        for image_or_link in images_or_links:
            text_list = old_text.split(f"{exclamation_point}[{image_or_link[0]}]({image_or_link[1]})", 1)
            if len(text_list) != 2:
                raise SyntaxError("Invalid markdown. Image text not closed.")
            if text_list[0] != "":
                new_nodes.append(
                    TextNode(
                        text_list[0],
                        text_type_text
                    )
                )
            new_nodes.append(
                TextNode(
                    image_or_link[0],
                    text_type,
                    image_or_link[1]
                )
            )
            old_text = text_list[1]
        if old_text != "":
            new_nodes.append(
                TextNode(
                    old_text,
                    text_type_text
                )
            )
    return new_nodes

def split_nodes_image(old_nodes):
    return split_nodes_helper(old_nodes, text_type_image, extract_markdown_images)

def split_nodes_link(old_nodes):
    return split_nodes_helper(old_nodes, text_type_link, extract_markdown_links)

def text_to_textnodes(text):
    nodes = []
    if text:
        nodes = [TextNode(text, text_type_text)]
    return split_nodes_delimiter(
                                split_nodes_delimiter(
                                    split_nodes_delimiter(
                                        split_nodes_link(
                                            split_nodes_image(nodes)
                                        ),
                                        "**",
                                        text_type_bold
                                    ),
                                    "*",
                                    text_type_italic
                                ),
                                "`",
                                text_type_code
                            )
