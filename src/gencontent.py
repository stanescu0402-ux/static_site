import os
import pathlib
from blocks_markdown import markdown_to_html_node


def generate_page(from_path: str, template_path: str, dest_path: str, basepath) -> None:
    print(f" * {from_path} {template_path} -> {dest_path}")
    from_file = open(from_path, "r")
    markdown_content = from_file.read()
    from_file.close()

    template_file = open(template_path, "r")
    template = template_file.read()
    template_file.close()

    node = markdown_to_html_node(markdown_content)
    html = node.to_html()

    title = extract_title(markdown_content)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)

    template = template.replace('href="/', f'href="{basepath}')
    template = template.replace('src="/', f'src="{basepath}')

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    to_file = open(dest_path, "w")
    to_file.write(template)


def extract_title(md: str) -> str:
    lines = md.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise ValueError("no title found")

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    contents = os.listdir(dir_path_content)
    for f in contents:
        path_content = os.path.join(dir_path_content,f)
        path_dest = os.path.join(dest_dir_path, f)
        print(path_content)
        print(path_dest)
        print("------------------------------------------------------")
        if os.path.isdir(path_content):
            generate_pages_recursive(path_content, template_path, path_dest, basepath)
        else:
            my_path = pathlib.Path(path_dest)
            new_path = my_path.with_suffix(".html")
            generate_page(path_content, template_path, str(new_path), basepath)