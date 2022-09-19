import tkinter as tk
from tkinter import ttk

from utils import HTMLBuilder


class TkinterTarget:
    """
    Core class to wrap Tkinter functionality and translate between an HTMLBuilder and
    tkinter code.
    """

    _REGISTERED_TAGS = {}
    """ Dictionary of registered tags with their associated handlers """

    @classmethod
    def component(cls, comp_class):
        """
        Decorator to register a class as a component tag with the same
        name as the class.

        NOTE: Class and tag names are converted to lowercase to match python's
        HTMLParser implementation.
        """
        if not issubclass(comp_class, Component):
            raise TypeError("Component classes must inherit from Component")
        
        cls._REGISTERED_TAGS[comp_class.__name__.lower()] = comp_class
        return comp_class
    
    @classmethod
    def basic(cls):
        """ Convenience method to create a basic TkinterTarget """
        root = tk.Tk()
        return cls(root)

    def __init__(self, root: tk.Tk, **kwargs):
        self.root = root
        self.options = kwargs
    
    def start(self):
        """ Start the Tkinter window """
        self.root.mainloop()
    
    def render(self, html: HTMLBuilder):
        """
        Render an HTMLBuilder object into a Tkinter window.
        """
        self._render(html.root, self.root)
        return self
    
    def _render(self, tag, parent=None):
        """ Render a tag """
        if parent is None:
            parent = self.root
        if tag.name in self._REGISTERED_TAGS:
            comp = self._REGISTERED_TAGS[tag.name](parent, **tag.kwargs)
            tk_widget = comp.render()
            for child in tag.children:
                self._render(child, tk_widget)
            tk_widget.pack()
            return tk_widget
        else:
            raise ValueError(f"Tag '{tag.name}' not registered")


class Component:
    """ Base class for all components """
    
    def __init__(self, parent, **kwargs):
        self.parent = parent
        self.options = kwargs
    
    def render(self):
        """ Render the component """
        raise NotImplementedError("Components must implement render()")


@TkinterTarget.component
class Frame(Component):
    """ Frame component """
    
    def render(self):
        return ttk.Frame(self.parent, **self.options)


@TkinterTarget.component
class Label(Component):
    """ Label component """
    
    def render(self):
        return ttk.Label(self.parent, **self.options)
