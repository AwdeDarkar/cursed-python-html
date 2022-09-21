from types import SimpleNamespace

class ImmutableDict(dict):
    """
    An immutable and hashable dictionary for state management

    TODO: Functions are _not_ hashable, but they are allowed
    for now. This will cause problems for tree comparison,
    but we could probably wrap them in a string representation.
    """

    def __setitem__(self, key, value):
        raise TypeError("ImmutableDict is immutable")

    def __delitem__(self, key):
        raise TypeError("ImmutableDict is immutable")

    def __hash__(self):
        return hash(frozenset(self.items()))
    
    def __eq__(self, other):
        return hash(self) == hash(other)

    def __repr__(self):
        return f"ImmutableDict({super().__repr__()})"

    def __str__(self):
        return f"ImmutableDict({super().__str__()})"
    
    def __getattribute__(self, name):
        if name not in ["keys"] and name in self.keys():
            return self[name]
        else:
            return super().__getattribute__(name)


def map_string(string, dict):
    """
    Replace characters in a string according to a mapping dictionary
    """
    return "".join(dict.get(c, c) for c in string)


class HTMLBuilder:
    """
    Function-chaining HTML builder.
    The 'cursed' syntax gets replaced with a chain of HTMLBuilder calls.
    """

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
    
    def param(self, name, func):
        self.top.kwargs[name] = func()
        return self
    
    def pop(self):
        self._stack.pop()
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
        
