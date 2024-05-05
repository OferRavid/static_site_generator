import unittest

from textnode import TextNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)
    
    def test_not_eq(self):
        node1 = TextNode("This is a text node", "bold")
        node2 = TextNode("This is also a text node", "italic")
        node3 = TextNode("This is a text node", "italic")
        node4 = TextNode("This is also a text node", "bold")
        self.assertNotEqual(node1, node2)
        self.assertNotEqual(node1, node3)
        self.assertNotEqual(node1, node4)
    
    def test_none_url(self):
        node = TextNode("This is a text node", "bold")
        self.assertTrue(node.url is None)
    
    def test_not_eq_missing_url(self):
        node_with_url = TextNode("Link text", "link", "https://www.boot.dev")
        node_without_url = TextNode("Link text", "link")
        self.assertTrue(node_without_url.url is None)
        self.assertNotEqual(node_with_url, node_without_url)


if __name__ == "__main__":
    unittest.main()
