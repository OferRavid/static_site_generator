import unittest

from markdown_blocks import (
    markdown_to_blocks,
    block_to_block_type,
    markdown_to_html_node,
    heading_block_to_html_node,
    quote_block_to_html_node,
    code_block_to_html_node,
    list_block_to_list_items,
    paragraph_block_to_html_node,
    block_type_h,
    block_type_p,
    block_type_q,
    block_type_c,
    block_type_ul,
    block_type_ol,
)


class TestMarkdownBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        markdown = """
This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        expected = [
            "This is **bolded** paragraph",
            "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
            "* This is a list\n* with items",
        ]
        actual = markdown_to_blocks(markdown)
        self.assertListEqual(expected, actual)
    
    def test_empty_markdown_to_blocks(self):
        markdown = ""
        expected = []
        actual = markdown_to_blocks(markdown)
        self.assertListEqual(expected, actual)
    
    def test_markdown_to_blocks_single(self):
        markdown = "This is a single paragraph"
        expected = ["This is a single paragraph"]
        actual = markdown_to_blocks(markdown)
        self.assertListEqual(expected, actual)
    
    def test_markdown_to_blocks_excessive(self):
        markdown = """
This is **bolded** paragraph



This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line






* This is a list
* with items
"""
        expected = [
            "This is **bolded** paragraph",
            "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
            "* This is a list\n* with items",
        ]
        actual = markdown_to_blocks(markdown)
        self.assertListEqual(expected, actual)
    
    def test_heading_block_to_block_types(self):
        h_block_1 = "# This is a heading"
        h_block_2 = "## This is a heading"
        h_block_3 = "### This is a heading"
        h_block_4 = "#### This is a heading"
        h_block_5 = "##### This is a heading"
        h_block_6 = "###### This is a heading"
        for block in [h_block_1, h_block_2, h_block_3, h_block_4, h_block_5, h_block_6]:
            expected = block_type_h
            actual = block_to_block_type(block)
            self.assertEqual(expected, actual)
    
    def test_code_block_to_block_types(self):
        block = "```\nThis is some code\n```"
        expected = block_type_c
        actual = block_to_block_type(block)
        self.assertEqual(expected, actual)
    
    def test_quote_block_to_block_types(self):
        block = "> This is a quote\n> Second line of the quote"
        expected = block_type_q
        actual = block_to_block_type(block)
        self.assertEqual(expected, actual)
    
    def test_ul__block_to_block_types(self):
        block = "* This is an unordered list\n* Second item in the list"
        expected = block_type_ul
        actual = block_to_block_type(block)
        self.assertEqual(expected, actual)
        block = "- This is an unordered list\n- Second item in the list"
        expected = block_type_ul
        actual = block_to_block_type(block)
        self.assertEqual(expected, actual)
    
    def test_ol_block_to_block_types(self):
        block = "1. This is an ordered list\n2. Second item in the list"
        expected = block_type_ol
        actual = block_to_block_type(block)
        self.assertEqual(expected, actual)
    
    def test_paragraph_block_to_block_types(self):
        block = "This is a normal paragraph"
        expected = block_type_p
        actual = block_to_block_type(block)
        self.assertEqual(expected, actual)
    
    def test_paragraph(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with *italic* text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_lists(self):
        md = """
- This is a list
- with items
- and *more* items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )
    
    def test_invalid_list(self):
        ulist = """
- 
- with items
- and *more* items
"""
        self.assertRaises(ValueError, list_block_to_list_items, ulist)
    
    def test_invalid_quote(self):
        quote = """
> This is a
- blockquote block
"""
        self.assertRaises(ValueError, quote_block_to_html_node, quote)
    
    def test_invalid_code(self):
        code = """
```
First line of code
Second line of code
``
"""
        self.assertRaises(ValueError, code_block_to_html_node, code)
    
    def test_invalid_heading(self):
        heading1 = "####### this is an invalid heading"
        heading2 = "#"
        heading3 = "# "
        self.assertRaises(SyntaxError, heading_block_to_html_node, heading1)
        self.assertRaises(SyntaxError, heading_block_to_html_node, heading2)
        self.assertRaises(ValueError, heading_block_to_html_node, heading3)
    
    def test_invalid_paragraph(self):
        paragraph = ""
        self.assertRaises(ValueError, paragraph_block_to_html_node, paragraph)


if __name__ == "__main__":
    unittest.main()
