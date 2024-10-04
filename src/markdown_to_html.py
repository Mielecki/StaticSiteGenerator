import os, pathlib

from block_markdown import markdown_to_htmlnode

def extract_title(markdown):
    splitted_markdown = markdown.split("\n\n")
    
    for line in splitted_markdown:
        if line.startswith("# "):
            return line.lstrip("#").strip()
    
    raise Exception("Title not found")

def generate_page(from_path, template_path, dest_path):
    with open(from_path) as markdown:
        markdown = markdown.read()
        title = extract_title(markdown)
        content = markdown_to_htmlnode(markdown).to_html()

    with open(template_path) as template:
        template = template.read()
        title_index = template.find("{{ Title }}")
        template = f"{template[:title_index]}{title}{template[title_index+11:]}"


        content_index = template.find("{{ Content }}")
        template = f"{template[:content_index]}{content}{template[content_index+13:]}"


    with open(os.path.join(dest_path, "index.html"), "w") as index:
        index.write(template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for item in os.listdir(dir_path_content):
        curr_path = os.path.join(dir_path_content, item)
        if os.path.isfile(curr_path):
            if str(pathlib.Path(curr_path))[-3:] == ".md":
                generate_page(curr_path, template_path, dest_dir_path)
        else:
            curr_dst = os.path.join(dest_dir_path, item)
            if not os.path.exists(curr_dst):
                os.mkdir(curr_dst)
            generate_pages_recursive(curr_path, template_path, curr_dst)