


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
            end_string += f'{k}="{val}" '
        return end_string

    def __repr__(self):
        print(f"""tag -> {self.tag}
value -> {self.value}
children -> {self.children}
props -> {self.props}""")