from types import SimpleNamespace

class BiDict(dict):
    """
    Bi-directional dictionary
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._inverse = {v: k for k, v in self.items()}

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self._inverse[value] = key
    
    def __delitem__(self, key):
        super().__delitem__(key)
        del self._inverse[self[key]]
    
    @property
    def inverse(self):
        return self._inverse


def map_string(string, dict):
    """
    Replace characters in a string according to a mapping dictionary
    """
    return "".join(dict.get(c, c) for c in string)


class HTMLBuilder:
    """ Function-chaining HTML builder; this is what the HTML syntax targets """

    def __init__(self):
        self._root = None
        self._stack = []
    
    @property
    def top(self):
        if len(self._stack) == 0:
            return None
        return self._stack[-1]
    
    @property
    def root(self):
        return self._root
    
    def tag(self, tag_name, *args, **kwargs):
        tag = SimpleNamespace()
        tag.args = args
        tag.kwargs = kwargs
        tag.name = tag_name
        tag.children = []
        if self._root is None:
            self._root = tag
        if self.top:
            tag.parent = self.top
            self.top.children.append(tag)
        self._stack.append(tag)
        return self
    
    def text(self, text):
        self.top.kwargs["text"] = text
        return self
    
    def pop(self):
        return self
    
    def _to_dict(self, tag):
        return {
            "tag": tag.name,
            "attrib": tag.kwargs,
            "text": tag.args[0] if len(tag.args) > 0 else None,
            "children": [self._to_dict(c) for c in tag.children]
        }
    
    def to_dict(self):
        return self._to_dict(self._root)
        
