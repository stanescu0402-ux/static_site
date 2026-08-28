


class HTMLNode():
    def __init__(self, tag= None, value= None, children= None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if (self.props == None):
            return ""
        end_string = ""
        for k, val in self.props.items():
            end_string += f' {k}="{val}"'
        return end_string

    def __repr__(self):
        return(f'HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})')


class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if (self.value == None):
            raise ValueError
        if (self.tag == None):
            return self.value
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'

    def __repr__(self):
        return(f'HTMLNode({self.tag}, {self.value}, {self.props})')


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag,None, children, props)
    def to_html(self):
        html = ""
        if (self.tag == None):
            raise ValueError
        if (self.children == None):
            raise ValueError("The children is missing")
        for child in self.children :
            html += child.to_html()
        return f'<{self.tag}>{html}</{self.tag}>'
        