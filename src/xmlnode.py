from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    out = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            out.append(node)
        else:
            text = node.text
            open = False
            temp_output = []
            splits = text.split(delimiter)
            for chunk in splits:
                if chunk == "":
                    open = not open
                    continue
                else:
                    temp_output.append(TextNode(chunk, text_type if open else TextType.PLAIN))
                    open = not open

            if not open:
                raise ValueError("The node provided does not contain valid markdown script")
            out.extend(temp_output)
    return out

def extract_markdown_images(text):
    images = re.findall(r"!\[(.+?)\]\((.+?)\)", text)
    extracted = []
    for image in images:
        extracted.append(image)
    return extracted

def extract_markdown_links(text):
    links = re.findall(r"(?<!\!)\[(.+?)\]\((.+?)\)", text)
    extracted = []
    for link in links:
        extracted.append(link)
    return extracted

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    out = []
    for node in old_nodes:
        if(node.text_type != TextType.PLAIN):
            out.append(node)
            continue
        images = extract_markdown_images(node.text)
        next = node.text
        for image in images:
            split = next.split(f"![{image[0]}]({image[1]})")
            if (split[0] != ""):
                out.append(TextNode(split[0], TextType.PLAIN))
            out.append(TextNode(image[0], TextType.IMAGE, url=image[1]))
            if(len(split) >1):
                next = split[1]
            else:
                next = ""
        if(next != ""):
            out.append(TextNode(next, TextType.PLAIN))
    return out

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    out = []
    for node in old_nodes:
        if(node.text_type != TextType.PLAIN):
            out.append(node)
            continue
        links = extract_markdown_links(node.text)
        next = node.text
        for link in links:
            split = next.split(f"[{link[0]}]({link[1]})")
            if (split[0] != ""):
                out.append(TextNode(split[0], TextType.PLAIN))
            out.append(TextNode(link[0], TextType.LINK, url=link[1]))
            if(len(split) >1):
                next = split[1]
            else:
                next = ""
        if(next != ""):
            out.append(TextNode(next, TextType.PLAIN))
    return out

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.PLAIN)]
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    return nodes
