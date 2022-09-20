import tkinter as tk
from tkinter import ttk

from utils import HTMLBuilder, ImmutableDict


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
    def component_tree_from_html(cls, html: HTMLBuilder):
        """
        Generate a component tree from an HTMLBuilder object.
        TODO: Implement child components
        """
        return cls.component_from_tag(html.root)

    @classmethod
    def component_from_tag(cls, tag):
        """ Generate a component from a tag """
        if tag.name in cls._REGISTERED_TAGS:
            return cls._REGISTERED_TAGS[tag.name](tag)
        else:
            raise ValueError(f"Tag '{tag.name}' not registered")
    
    @classmethod
    def basic(cls):
        """ Convenience method to create a basic TkinterTarget """
        root = tk.Tk()
        return cls(root)
    
    @classmethod
    def main(cls, **kwargs):
        """ Convenience method to create a TkinterTarget with a 'main' component """
        root = tk.Tk()
        tktarget = cls(root)
        main = cls.component_tree_from_html(
            HTMLBuilder().tag("main", **kwargs).pop()
        )

        tktarget.mount_to_root(component=main)

        return tktarget

    def __init__(self, root: tk.Tk, **kwargs):
        self.root = root
        self.options = kwargs
    
    def mount_to_root(self, component):
        """ Mount a component as the top-level frame of the Tkinter window """
        print(f"Mounting {component} to {self.root}")
        component.component_will_mount(self.root)
        component.mount(self.root)
        component.component_did_mount(self.root)

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
            comp = self._REGISTERED_TAGS[tag.name](tag)
            return comp.render(parent, **tag.kwargs)
        else:
            raise ValueError(f"Tag '{tag.name}' not registered")


class Component:
    """ Base class for all components """
    
    @classmethod
    def get_initial_state(cls):
        """ Get the initial state of the component """
        return {}

    def __init__(self, tag):
        self.props = ImmutableDict({
            **tag.kwargs,
        })

        self.state = ImmutableDict({
            **self.get_initial_state(),
        })

        self.tag = tag
        self.children = [
            TkinterTarget.component_from_tag(child)
            for child in tag.children
        ]

        self.render_root = None
        self.widget = None
        self.parent_widget = None
    
    def change_props(self, **props):
        """ Change the component's props """
        old = self.props
        self.props = ImmutableDict({
            **props,
        })

        if self.props != old:
            self.update()
            self.component_did_update()

    def set_state(self, update):
        """ Update the component's state """
        old = self.state
        self.state = ImmutableDict({
            **self.state,
            **update,
        })

        if old != self.state:
            self.update()
            self.component_did_update()
    
    def component_will_mount(self, widget):
        pass

    def component_did_mount(self, widget):
        pass

    def component_will_unmount(self):
        pass

    def component_did_update(self):
        pass

    def mount(self, widget):
        """ Mount the component """
        self.parent_widget = widget
        self.render_root = TkinterTarget.component_tree_from_html(self.render())
        self.render_root.component_will_mount(widget)
        self.widget = self.render_root.mount(widget)
        self.render_root.component_did_mount(widget)

        for child in self.children:
            child.component_will_mount(self.widget)
            child.mount(self.widget)
            child.component_did_mount(self.widget)
        
        return self.widget

    def update(self):
        """ Update the component """
        if self.widget is None:
            return
        self.render_root.component_will_unmount()
        self.render_root = TkinterTarget.component_tree_from_html(self.render())
        self.widget.destroy()
        self.render_root.component_will_mount(self.parent_widget)
        self.widget = self.render_root.mount(self.parent_widget)
        self.render_root.component_did_mount(self.parent_widget)


    def render(self) -> HTMLBuilder:
        """ Render the component to an HTMLBuilder """
        raise NotImplementedError("Components must implement render()")


class BaseComponent(Component):
    """
    Base components are components that wrap a Tkinter widget;
    they do not have a 'render' method and instead mount directly.
    """

    def get_widget(self, widget):
        """ Get the widget to render """
        raise NotImplementedError("BaseComponents must implement get_widget()")

    def render(self):
        raise TypeError("Base components do not implement render()")
    
    def mount(self, widget):
        """ Mount the component """
        self.widget = self.get_widget(widget)

        for child in self.children:
            child.component_will_mount(self.widget)
            child.mount(self.widget)
            child.component_did_mount(self.widget)

        self.widget.pack()       
        return self.widget


@TkinterTarget.component
class Frame(BaseComponent):
    """ Frame component """

    def get_widget(self, widget):
        """ Mount the component """
        return ttk.Frame(widget, **self.props)


@TkinterTarget.component
class Label(BaseComponent):
    """ Label component """

    def get_widget(self, widget):
        """ Mount the component """
        return ttk.Label(widget, **self.props)


@TkinterTarget.component
class Button(BaseComponent):
    """ Button component """

    def get_widget(self, widget):
        """ Mount the component """
        return ttk.Button(widget, **self.props)