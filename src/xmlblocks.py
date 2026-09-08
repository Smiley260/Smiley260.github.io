from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    U_LIST = "unordered list"
    O_LIST = "ordered list"

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    output = []
    for block in blocks:
        stripped_block = block.strip()
        if stripped_block != "":
            output.append(stripped_block)

    return output

def block_to_block_type(block):
    if re.match(r"^#{1,6} ", block):
        return BlockType.HEADING
    elif re.match(r"^`{3}\n", block) and re.search(r"\n`{3}$", block):
        return BlockType.CODE
    elif re.match(r"^(> ?.*\n?)+$", block):
        return BlockType.QUOTE
    elif re.match(r"^(- .*\n?)+$", block):
        return BlockType.U_LIST
    else:
        lines = block.split("\n")
        ordered = True
        prev = 0
        for line in lines:
            start = re.search(r"^\d+\. ", line)
            if start and int(start.group()[:-2]) == prev + 1:
                prev += 1
            else:
                ordered = False
        if ordered:
            return BlockType.O_LIST
        else:
            return BlockType.PARAGRAPH
    
def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if re.match(r"^# ", block):
            return re.split(r"^# ", block)[1].strip()
    raise ValueError("The provided markdown does no contain a title")