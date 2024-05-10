import unittest

from textnode import (
    TextNode,
    text_node_to_html_node,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_link,
    text_type_image,
)

from inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)


class TestInlineMarkdown(unittest.TestCase):
    def test_inline_code(self):
        node = TextNode("This is text with a `code block` word", text_type_text)
        actual = split_nodes_delimiter([node], "`", text_type_code)
        expected = [
                        TextNode("This is text with a ", text_type_text),
                        TextNode("code block", text_type_code),
                        TextNode(" word", text_type_text),
                    ]
        self.assertEqual(expected, actual)
    
    def test_inline_bold(self):
        node = TextNode("This is text with a **bold** word", text_type_text)
        actual = split_nodes_delimiter([node], "**", text_type_bold)
        expected = [
                        TextNode("This is text with a ", text_type_text),
                        TextNode("bold", text_type_bold),
                        TextNode(" word", text_type_text),
                    ]
        self.assertEqual(expected, actual)
    
    def test_inline_italic(self):
        node = TextNode("This is text with an *italic* word", text_type_text)
        actual = split_nodes_delimiter([node], "*", text_type_italic)
        expected = [
                        TextNode("This is text with an ", text_type_text),
                        TextNode("italic", text_type_italic),
                        TextNode(" word", text_type_text),
                    ]
        self.assertEqual(expected, actual)
    
    def test_inline_once_multiple_delim(self):
        node = TextNode("This text has an *italic* word and a **bold** word", text_type_text)
        expected = [
                        TextNode("This text has an *italic* word and a ", text_type_text),
                        TextNode("bold", text_type_bold),
                        TextNode(" word", text_type_text),
                    ]
        actual = split_nodes_delimiter([node], "**", text_type_bold)
        self.assertEqual(expected, actual)
    
    def test_inline_multiple_delim(self):
        node = TextNode("This text has an *italic* word and a **bold** word", text_type_text)
        expected = [
                        TextNode("This text has an ", text_type_text),
                        TextNode("italic", text_type_italic),
                        TextNode(" word and a ", text_type_text),
                        TextNode("bold", text_type_bold),
                        TextNode(" word", text_type_text),
                    ]
        nodes = split_nodes_delimiter([node], "**", text_type_bold)
        actual = split_nodes_delimiter(nodes, "*", text_type_italic)
        self.assertEqual(expected, actual)
    
    def test_inline_multiple(self):
        node = TextNode("This is text with a `code block` word", text_type_text)
        node2 = TextNode("This is a simple text", text_type_text)
        node3 = TextNode("This is a bold text", text_type_bold)
        node4 = TextNode("This is text with `code block1` word and `code block2` word", text_type_text)
        actual = split_nodes_delimiter([node, node2, node3, node4], "`", text_type_code)
        expected = [
                        TextNode("This is text with a ", text_type_text),
                        TextNode("code block", text_type_code),
                        TextNode(" word", text_type_text),
                        TextNode("This is a simple text", text_type_text),
                        TextNode("This is a bold text", text_type_bold),
                        TextNode("This is text with ", text_type_text),
                        TextNode("code block1", text_type_code),
                        TextNode(" word and ", text_type_text),
                        TextNode("code block2", text_type_code),
                        TextNode(" word", text_type_text),
                    ]
        self.assertEqual(expected, actual)
    
    def test_inline_invalid(self):
        node = TextNode("This is text with a `code block word", text_type_text)
        self.assertRaises(SyntaxError, split_nodes_delimiter, [node], "`", text_type_code)
    
    def test_inline_invalid_multiple_nodes(self):
        node2 = TextNode("This is text with a `code block word", text_type_text)
        node = TextNode("This is text with a `code block` word", text_type_text)
        self.assertRaises(SyntaxError, split_nodes_delimiter, [node, node2], "`", text_type_code)
    
    def test_extract_image(self):
        text = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"
        actual = extract_markdown_images(text)
        expected = [("image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"), ("another", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png")]
        self.assertEqual(expected, actual)
    
    def test_extract_image_none(self):
        text = "This is text with no image"
        actual = extract_markdown_images(text)
        expected = []
        self.assertEqual(expected, actual)
    
    def test_extract_link(self):
        text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
        actual = extract_markdown_links(text)
        expected = [("link", "https://www.example.com"), ("another", "https://www.example.com/another")]
        self.assertEqual(expected, actual)
    
    def test_extract_link_none(self):
        text = "This is text with no links"
        actual = extract_markdown_links(text)
        expected = []
        self.assertEqual(expected, actual)
    
    def test_split_nodes_image(self):
        node = TextNode(
            "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
            text_type_text,
        )
        expected = [
            TextNode("This is text with an ", text_type_text),
            TextNode("image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
            TextNode(" and another ", text_type_text),
            TextNode(
                "second image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png"
            ),
        ]
        actual = split_nodes_image([node])
        self.assertEqual(expected, actual)
    
    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev) with text that follows",
            text_type_text,
        )
        expected = [
            TextNode("This is text with a ", text_type_text),
            TextNode("link", text_type_link, "https://boot.dev"),
            TextNode(" and ", text_type_text),
            TextNode("another link", text_type_link, "https://blog.boot.dev"),
            TextNode(" with text that follows", text_type_text),
        ]
        actual = split_nodes_link([node])
        self.assertEqual(expected, actual)
    
    def test_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)"
        expected = [
            TextNode("This is ", text_type_text),
            TextNode("text", text_type_bold),
            TextNode(" with an ", text_type_text),
            TextNode("italic", text_type_italic),
            TextNode(" word and a ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" and an ", text_type_text),
            TextNode("image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
            TextNode(" and a ", text_type_text),
            TextNode("link", text_type_link, "https://boot.dev"),
        ]
        actual = text_to_textnodes(text)
        self.assertEqual(expected, actual)
    
    def test_text_to_textnodes_no_text(self):
        text = ""
        expected = []
        actual = text_to_textnodes(text)
        self.assertEqual(expected, actual)



if __name__ == "__main__":
    unittest.main()
