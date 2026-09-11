

class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        output=""
        if self.props is not None:
            for key,value in self.props.items():
                output = output + f" {key}=\"{value}\""
        return output
    
    def __repr__(self):
        return f"HTMLNode:\n- tag: {self.tag}\n- value: {self.value}\n- children: {self.children}\n- props: {self.props_to_html()}"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, children=None, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError()
        elif self.tag is None:
            return self.value
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        
    def __repr__(self):
        return f"HTMLNode:\n- tag: {self.tag}\n- value: {self.value}\n- props: {self.props_to_html()}"
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, value=None, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Parent node has no tag")
        elif self.children is None:
            raise ValueError("Parent node has no children")
        else:
            totalhtml = ""
            for child in self.children:
                totalhtml += child.to_html()
            return f"<{self.tag}>{totalhtml}</{self.tag}>"
        