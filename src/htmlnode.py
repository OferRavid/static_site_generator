class HTMLNode:
    def __init__(self, tag=None, value=None, children=[], props={}):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError("Method isn't implemented yet. Please implement this method.")
    
    def props_to_html(self):
        result = ""
        for k, v in self.props.items():
            result += f" {k}=\"{v}\""
        return result
    
    def __repr__(self):
        return f"tag: {self.tag}\nvalue: {self.value}\nchildren: {self.children}\nprops: {self.props_to_html()}\n"


class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props={}):
        super().__init__(tag, value, props=props)
    
    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes require a value!")
        if not self.tag:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props={}):
        super().__init__(tag=tag, children=children, props=props)
    
    def to_html(self):
        if not self.tag:
            raise ValueError("Parent node must have a tag.")
        if not self.children:
            raise ValueError("Parent node requires children!")
        children_html = ""
        for child in self.children:
            children_html += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"
