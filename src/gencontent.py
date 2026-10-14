import os
import pathlib
from blocks_markdown import markdown_to_html_node


def generate_page(from_path: str, template_path: str, dest_path: str, basepath) -> None:
    print(f" * {from_path} {template_path} -> {dest_path}")
    with open(from_path, "r") as from_file:
        markdown_content = from_file.read()

    with open(template_path, "r") as template_file:
        template = template_file.read()

    node = markdown_to_html_node(markdown_content)
    html = node.to_html()

    title = extract_title(markdown_content)
    
    # 1. Clean up basepath safely
    clean_basepath = basepath.rstrip("/")
    target_prefix = f"{clean_basepath}/" if clean_basepath else "/"

    # 2. Inject Title and HTML Content into Template
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)

    # 3. Apply basepath replacements to the TEMPLATE (e.g. stylesheet links)
    template = template.replace('href="/', f'href="{target_prefix}')
    template = template.replace('src="/', f'src="{target_prefix}')

    # 4. ALSO apply basepath replacements to the MARKDOWN HTML CONTENT (e.g. images & internal links)
    template = template.replace(html, html.replace('href="/', f'href="{target_prefix}').replace('src="/', f'src="{target_prefix}'))

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    with open(dest_path, "w") as to_file:
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
        path_content = os.path.join(dir_path_content, f)
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