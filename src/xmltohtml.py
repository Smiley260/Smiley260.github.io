from htmlnode import ParentNode
from textnode import TextNode, TextType, text_node_to_html_node
from xmlblocks import markdown_to_blocks, block_to_block_type, BlockType
from xmlnode import text_to_textnodes
import re

def markdown_to_html_node(markdown):
    markdown_blocks = markdown_to_blocks(markdown)
    block_html = []
    for block in markdown_blocks:
        block_html.append(block_to_html(block, block_to_block_type(block)))
    parent_div = ParentNode(tag="div", children=block_html)
    return parent_div

#input: tuple containing block text, and block type
#returns html node created from block
def block_to_html(block, block_type):
    match block_type:
        case BlockType.HEADING:
            html_parent = heading_to_html(block)
        case BlockType.CODE:
            html_parent = code_to_html(block)
        case BlockType.QUOTE:
            html_parent = blockquote_to_html(block, r"> ?", "blockquote")
        case BlockType.U_LIST:
            html_parent = list_to_html(block, r"- ", "ul", "li")
        case BlockType.O_LIST:
            html_parent = list_to_html(block, r"\d+\. ", "ol", "li")
        case BlockType.PARAGRAPH:
            html_parent = paragraph_to_html(block, "p")
        case _:
            raise ValueError("Provided xml block is not a valid type")

    return html_parent


#input: block text for a heading
#returns a heading node
def heading_to_html(block_text):
    text = re.split(r"#{1,6} ", block_text, maxsplit=1)[1]
    heading = re.search(r"^#{1,6} ", block_text)
    if heading:
        heading_val = len(heading.group()[:-1])
    else:
        raise ValueError("Provided markdown does not have the correct block format")
    html_parent = paragraph_to_html(text, f"h{heading_val}")
    return html_parent


#input:
#   block_text - block text for a code block
#returns:
#   html_parent - a code block HTML node
def code_to_html(block_text):
    text = block_text[4:-3]
    text_node = TextNode(text, TextType.CODE)
    code_html =  text_node_to_html_node(text_node)
    html_parent = ParentNode(tag="pre", children=[code_html])
    return html_parent


#input: 
#   text        - block text for the un-split list
#   regex       - the regex string to determine the start of a line
#   list_tag    - the parent HTML tag for the list node
#returns:
#   html_parent - the parent HTML node containing the list
def blockquote_to_html(text, regex, list_tag):
    text_lines = re.split(r"\n"+regex, text)
    text_lines[0] = re.split(r"^"+regex, text_lines[0], maxsplit=1)[1]
    lines = "\n".join(text_lines)
    html_parent = paragraph_to_html(lines, list_tag)
    return html_parent

#input: 
#   text        - block text for the un-split list
#   regex       - the regex string to determine the start of a line
#   list_tag    - the parent HTML tag for the list node
#   line_tag    - the HTML tag for each line item
#returns:
#   html_parent - the parent HTML node containing the list
def list_to_html(text, regex, list_tag, line_tag):
    text_lines = re.split(r"\n"+regex, text)
    text_lines[0] = re.split(r"^"+regex, text_lines[0], maxsplit=1)[1]
    lines = []
    for line in text_lines:
        lines.append(paragraph_to_html(line, line_tag))
    html_parent = ParentNode(tag=list_tag, children=lines)
    return html_parent

#input: 
#   block_text  - block text for a paragraph
#   type        - the tag to use when creating the html node
#returns:
#   html_parent - a HTML node with the request tag type
def paragraph_to_html(block_text, type):

    text_nodes = text_to_textnodes(block_text.replace("\n", " ")) if type != "blockquote" else text_to_textnodes(block_text)
    html_nodes = []
    for text_node in text_nodes:
        html_nodes.append(text_node_to_html_node(text_node))
    html_parent = ParentNode(tag=type, children=html_nodes)
    return html_parent