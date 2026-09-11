import unittest
from textnode import TextNode, TextType, text_node_to_html_node # type: ignore

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_noteq(self):
        node = TextNode("This is a text node", TextType.BOLD, url="whatever")
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)
        
    def test_noteq2(self):
        node = TextNode("This is a text node", TextType.BOLD, url="whatever")
        node2 = TextNode("This is not? a text node", TextType.BOLD, url="whatever")
        self.assertNotEqual(node, node2)
        
    def test_noteq3(self):
        node = TextNode("This is a text node", TextType.BOLD, url="whatever")
        node2 = TextNode("This is a text node", TextType.ITALIC, url="whatever")
        self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.PLAIN)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        
    def test_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")
        
    def test_italic(self):
        node = TextNode("This is a itallics node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a itallics node")

    def test_code(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node")
    
    def test_link(self):
        node = TextNode("This is a link node", TextType.LINK, "https://link")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link node")
        self.assertEqual(html_node.props, ["href=\"https://link\""])

    def test_image(self):
        node = TextNode("This is an image node", TextType.IMAGE, "https://link")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, ["src=\"https://link\"", "alt=\"This is an image node\""])


if __name__ == "__main__":
    unittest.main()