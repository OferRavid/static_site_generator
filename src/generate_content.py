import os
from pathlib import Path
from markdown_blocks import markdown_to_html_node


def extract_title(markdown):
    for line in markdown.split("\n"):
        if line.startswith("# "):
            return line[2:]
    raise ValueError("Invalid markdown: missing h1 header.")

def generate_page(from_path, template_path, dest_path, basepath):
    if not os.path.exists(from_path) or not os.path.exists(template_path):
        raise FileNotFoundError("Something's wrong with the paths provided...")
    print(f"Generating page from {from_path} to {dest_path} using template: {template_path}")
    with open(from_path) as markdown_file:
        markdown = markdown_file.read()
    with open(template_path) as template_file:
        template = template_file.read()
    content = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    page = template.replace(
        "{{ Title }}", title).replace(
            "{{ Content }}", content).replace(
                'href="/', 'href="' + basepath).replace(
                    'src="/', 'src="' + basepath)
    with open(dest_path, 'w') as html:
        html.write(page)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    if not os.path.exists(dir_path_content) or not os.path.exists(template_path) or not os.path.exists(dest_dir_path):
        raise FileNotFoundError("Something's wrong with the paths provided...")
    for dir_or_file in os.listdir(dir_path_content):
        source_dir_or_file = os.path.join(dir_path_content, dir_or_file)
        target_dir_or_file = os.path.join(dest_dir_path, dir_or_file)
        if os.path.isdir(source_dir_or_file):
            try:
                os.mkdir(target_dir_or_file)
            except FileExistsError:
                print(f"The {target_dir_or_file} directory already exists. Remove it and try again.")
                return
            except FileNotFoundError:
                print("Something is wrong with the path provided. Check it and try again.")
                return
            generate_pages_recursive(source_dir_or_file, template_path, target_dir_or_file, basepath)
        elif os.path.isfile(source_dir_or_file):
            dest_path = Path(target_dir_or_file).with_suffix(".html")
            generate_page(source_dir_or_file, template_path, dest_path, basepath)

