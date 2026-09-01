from textnode import TextNode, TextType # type: ignore
from enum import Enum
import os
import shutil

print("hello world")

def recursive_copy(src, dest):
    if os.path.exists(dest):
        shutil.rmtree(dest)
    os.mkdir(dest)
    if not (os.path.exists(src)):
        raise ValueError("One or more of the provided file paths don't exist or couldn;t be created")

    contents = os.listdir(src)

    for item in contents:
        item_path = os.path.join(src,item)
        if os.path.isfile(item_path):
            shutil.copy(item_path, dest)
        else:
            recursive_copy(item_path, os.path.join(dest, item))

    return dest

def main():
    node = TextNode("test link", TextType.LINK, "https://www.boot.dev")
    print(node)

    print(recursive_copy("static", "public"))

main()
