from htmlnode import *
from copy_files import copy_static_to_public
from markdown_to_html import generate_pages_recursive

def main():
    copy_static_to_public()
    generate_pages_recursive("content", "template.html", "public")

if __name__ == "__main__":
    main()