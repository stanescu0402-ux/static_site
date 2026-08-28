from textnode import TextType, TextNode, LeafNode
import re



def text_to_textnodes(text: str) -> list[TextNode]:
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    if text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    if text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    if text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    if text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, "href")
    if text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "", ["src", "alt"])
    raise Exception("can't do that bro")

def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes


def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        remaining_text = old_node.text
        image_list = extract_markdown_images(remaining_text)
        if len(image_list) == 0:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        for image_info in image_list :
            sections = remaining_text.split(f"![{image_info[0]}]({image_info[1]})", 1)
            if len(sections) % 2 == 1:
                raise ValueError("invalid markdown, formatted section not closed")
            if sections[0] != "":
                split_nodes.append(TextNode(sections[0], TextType.TEXT))
            split_nodes.append(TextNode(image_info[0], TextType.IMAGE, image_info[1]))
            remaining_text = sections[1]
        if sections[1] != "":
            split_nodes.append(TextNode(sections[1], TextType.TEXT))
        new_nodes.extend(split_nodes)
    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        remaining_text = old_node.text
        link_list = extract_markdown_links(remaining_text)
        if len(link_list) == 0:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        for link_info in link_list :
            sections = remaining_text.split(f"[{link_info[0]}]({link_info[1]})", 1)
            if len(sections) % 2 == 1:
                raise ValueError("invalid markdown, formatted section not closed")
            if sections[0] != "":
                split_nodes.append(TextNode(sections[0], TextType.TEXT))
            split_nodes.append(TextNode(link_info[0], TextType.LINK, link_info[1]))
            remaining_text = sections[1]
        if sections[1] != "":
            split_nodes.append(TextNode(sections[1], TextType.TEXT))
        new_nodes.extend(split_nodes)
    return new_nodes



