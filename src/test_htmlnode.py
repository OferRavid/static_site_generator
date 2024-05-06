import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_empty_node(self):
        node = HTMLNode()
        self.assertTrue(not node.tag and
                        not node.value and
                        not node.children and
                        not node.props)
        self.assertEqual(node.props_to_html(), "")
    
    def test_repr(self):
        node = HTMLNode("a", "Link", [], {"href": "https://www.boot.dev"})
        expected = "tag: a\nvalue: Link\nchildren: []\nprops:  href=\"https://www.boot.dev\"\n"
        actual = node.__repr__()
        self.assertEqual(expected, actual)
    
    def test_props_to_html(self):
        node = HTMLNode("a", "Link", [], {"href": "https://www.boot.dev", "target": "_blank"})
        expected = " href=\"https://www.boot.dev\" target=\"_blank\""
        actual = node.props_to_html()
        self.assertEqual(expected, actual)
    
    def test_leaf_node(self):
        node = LeafNode("p", "This is a paragraph of text.")
        expected = "<p>This is a paragraph of text.</p>"
        actual = node.to_html()
        self.assertEqual(expected, actual)
    
    def test_leaf_no_value(self):
        leaf = LeafNode()
        self.assertRaises(ValueError, leaf.to_html)

    def test_leaf_link(self):
        leaf = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        expected = "<a href=\"https://www.google.com\">Click me!</a>"
        actual = leaf.to_html()
        self.assertEqual(expected, actual)
    
    def test_leaf_no_tag(self):
        leaf = LeafNode(value="Raw text")
        expected = "Raw text"
        actual = leaf.to_html()
        self.assertEqual(expected, actual)
    
    def test_parent_node(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        expected = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        actual = node.to_html()
        self.assertEqual(expected, actual)
    
    def test_nested_parents(self):
        p1 = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        link_node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        p2 = ParentNode(
            "p",
            [
                LeafNode(None, "Normal text2"),
                LeafNode("i", "italic text2"),
                link_node,
                LeafNode(None, "Normal text2"),
            ],
        )
        header = LeafNode("h1", "Header for this test")
        parent = ParentNode(
            "body",
            [
                header,
                p1,
                p2,
            ]
        )
        expected = "<body><h1>Header for this test</h1><p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p><p>Normal text2<i>italic text2</i><a href=\"https://www.google.com\">Click me!</a>Normal text2</p></body>"
        actual = parent.to_html()
        self.assertEqual(expected, actual)

if __name__ == "__main__":
    unittest.main()
