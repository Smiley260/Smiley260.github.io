from textnode import TextNode, TextType # type: ignore
from xmltohtml import markdown_to_html_node
from xmlblocks import extract_title
from enum import Enum
import os
import shutil
import sys

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

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    md = open(from_path)
    markdown = md.read()

    html = open(template_path)
    template = html.read()

    generated_html = markdown_to_html_node(markdown)
    html_string = generated_html.to_html()
    title = extract_title(markdown)

    output = template.replace(r"{{ Title }}", title)
    output = output.replace(r"{{ Content }}", html_string)
    output = output.replace(r"href=\"/", f"href=\"{basepath}")
    output = output.replace(r"src=\"/", f"src=\"{basepath}")

    with open(dest_path, "w") as out:
        out.write(output)

    return

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    
    contents = os.listdir(dir_path_content)
    
    for item in contents:
        item_path = os.path.join(dir_path_content, item)
        dest_path = os.path.join(dest_dir_path, item)
        if os.path.isfile(item_path):
            ext_split = os.path.splitext(item)
            if ext_split[1] == ".md":
                dest_path = os.path.join(dest_dir_path, ext_split[0] + ".html")
                generate_page(item_path, template_path, dest_path, basepath)
        elif not os.path.isfile(item_path):
            os.mkdir(dest_path)
            generate_pages_recursive(item_path, template_path, dest_path, basepath)

def main():
    basepath = sys.argv[1] if len(sys.argv[1]) > 1 else "/"
    

    recursive_copy("static", "docs")

    generate_pages_recursive(f"{basepath}content/", f"{basepath}template.html", f"{basepath}docs/", basepath)
main()
