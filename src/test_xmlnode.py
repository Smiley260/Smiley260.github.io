import unittest
from textnode import TextNode, TextType, text_node_to_html_node # type: ignore
from xmlnode import split_nodes_delimiter, extract_markdown_images, text_to_textnodes, extract_markdown_links, split_nodes_image, split_nodes_link # type: ignore


class TestXmlNode(unittest.TestCase):
    def test_mid(self):
        node = TextNode("This is a **text** node", TextType.PLAIN)
        split_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        nodes = [TextNode("This is a ", TextType.PLAIN), TextNode("text", TextType.BOLD), TextNode(" node", TextType.PLAIN)]
        self.assertEqual(split_nodes, nodes)

    def test_start(self):
        node = TextNode("**This** is a text node", TextType.PLAIN)
        split_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        nodes = [TextNode("This", TextType.BOLD), TextNode(" is a text node", TextType.PLAIN)]
        self.assertEqual(split_nodes, nodes)
        
    def test_end(self):
        node = TextNode("This is a text **node**", TextType.PLAIN)
        split_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        nodes = [TextNode("This is a text ", TextType.PLAIN), TextNode("node", TextType.BOLD)]
        self.assertEqual(split_nodes, nodes)
        
    def test_multiple(self):
        node = TextNode("This **is** a **text** node", TextType.PLAIN)
        split_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        nodes = [TextNode("This ", TextType.PLAIN), TextNode("is", TextType.BOLD), TextNode(" a ", TextType.PLAIN), TextNode("text", TextType.BOLD), TextNode(" node", TextType.PLAIN)]
        self.assertEqual(split_nodes, nodes)

    def test_multiple_start(self):
        node = TextNode("**This is** a **text** node", TextType.PLAIN)
        split_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        nodes = [TextNode("This is", TextType.BOLD), TextNode(" a ", TextType.PLAIN), TextNode("text", TextType.BOLD), TextNode(" node", TextType.PLAIN)]
        self.assertEqual(split_nodes, nodes)
        
    def test_multiple_end(self):
        node = TextNode("This **is** a **text node**", TextType.PLAIN)
        split_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        nodes = [TextNode("This ", TextType.PLAIN), TextNode("is", TextType.BOLD), TextNode(" a ", TextType.PLAIN), TextNode("text node", TextType.BOLD)]
        self.assertEqual(split_nodes, nodes)
                
    def test_multiple_both(self):
        node = TextNode("**This is** a **text node**", TextType.PLAIN)
        split_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        nodes = [TextNode("This is", TextType.BOLD), TextNode(" a ", TextType.PLAIN), TextNode("text node", TextType.BOLD)]
        self.assertEqual(split_nodes, nodes)
    
    def test_odd_end(self):
        node = TextNode("This is** a **text node**", TextType.PLAIN)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "**", TextType.BOLD)
    
    def test_odd_start(self):
        node = TextNode("**This is** a **text node", TextType.PLAIN)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "**", TextType.BOLD)
     
    def test_unchanged(self):
        node = TextNode("**This is** a **text node**", TextType.CODE)
        split_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(split_nodes[0], node)


    def test_multiple_array(self):
        node1 = TextNode("**This is** a **text node**", TextType.PLAIN)
        node2 = TextNode("This is a **code node**", TextType.CODE)
        node3 = TextNode("**This is** a second **text node**", TextType.PLAIN)
        split_nodes = split_nodes_delimiter([node1, node2, node3], "**", TextType.BOLD)
        nodes = [TextNode("This is", TextType.BOLD), TextNode(" a ", TextType.PLAIN), TextNode("text node", TextType.BOLD), TextNode("This is a **code node**", TextType.CODE), TextNode("This is", TextType.BOLD), TextNode(" a second ", TextType.PLAIN), TextNode("text node", TextType.BOLD)]
        self.assertEqual(split_nodes, nodes)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with an [image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
        
    def test_extract_markdown_links_negative(self):
        matches = extract_markdown_links(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([], matches)

    def test_extract_markdown_images_empty(self):
        matches = extract_markdown_images(
            "This is text with an ![](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([], matches)

    def test_extract_markdown_images_multiple(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and ![image2](https://i.imgur.com/zjjcJKZ.png two electric boogaloo)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png"), ("image2", "https://i.imgur.com/zjjcJKZ.png two electric boogaloo")], matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode("second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

        
    def test_split_images_end(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) so hows about that?",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
                TextNode(" so hows about that?", TextType.PLAIN),
            ],
            new_nodes,
        )

          
    def test_split_images_start(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) so hows about that?",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
                TextNode(" so hows about that?", TextType.PLAIN),
            ],
            new_nodes,
        )

          
    def test_split_textnodes(self):
        node = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
            
        new_nodes = text_to_textnodes(node)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.PLAIN),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.PLAIN),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.PLAIN),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.PLAIN),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.PLAIN),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes,
        )
          
    def test_split_textnodes_2(self):
        node = "This is **text** with an _italic and not bold_ word and a `code block` and an ![obi _wan_ image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
            
        new_nodes = text_to_textnodes(node)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.PLAIN),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.PLAIN),
                TextNode("italic and not bold", TextType.ITALIC),
                TextNode(" word and a ", TextType.PLAIN),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.PLAIN),
                TextNode("obi _wan_ image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.PLAIN),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes,
        )

if __name__ == "__main__":
    unittest.main()