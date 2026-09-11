import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode # type: ignore

class TestTextNode(unittest.TestCase):
    def test_props(self):
        node = HTMLNode("h1", "spleens")
        self.assertEqual("", node.props_to_html())

    
    def test_props2(self):
        node = HTMLNode("a", "france", props={"href": "Somewhere on wikipedia", "target": "_blank",})
        self.assertEqual(" href=\"Somewhere on wikipedia\" target=\"_blank\"", node.props_to_html())

    def test_props3(self):
        node = HTMLNode("a", "france 2", props={"href": "Somewhere else on wikipedia",})
        self.assertEqual(" href=\"Somewhere else on wikipedia\"", node.props_to_html())

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "france 2", props={"href": "Somewhere else on wikipedia",})
        self.assertEqual(node.to_html(), "<a href=\"Somewhere else on wikipedia\">france 2</a>")

    def test_leaf_to_html_a2(self):
        node = LeafNode("a", "france 2", props={"href": "Somewhere else on wikipedia", "target": "_blank",})
        self.assertEqual(node.to_html(), "<a href=\"Somewhere else on wikipedia\" target=\"_blank\">france 2</a>")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

        
    def test_to_html_with_many_children(self):
        child_node1 = LeafNode("span", "child1")
        child_node2 = LeafNode("b", "child2")
        child_node3 = LeafNode("i", "child3")
        child_node4 = LeafNode("p", "child4")
        parent_node = ParentNode("div", [child_node1, child_node2, child_node3, child_node4])
        self.assertEqual(parent_node.to_html(), "<div><span>child1</span><b>child2</b><i>child3</i><p>child4</p></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_layered_grandchildren(self):
        grandchild_node1 = LeafNode("i", "grandchild1")
        grandchild_node2 = LeafNode("b", "grandchild2")
        grandchild_node1_1 = LeafNode("i", "grandchild1_1")
        grandchild_node1_2 = LeafNode("b", "grandchild1_2")
        child_node1 = ParentNode("span", [grandchild_node1, grandchild_node2])
        child_node2 = ParentNode("span", [grandchild_node1_1, grandchild_node1_2])
        parent_node = ParentNode("div", [child_node1, child_node2])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><i>grandchild1</i><b>grandchild2</b></span><span><i>grandchild1_1</i><b>grandchild1_2</b></span></div>",
        )