import re
import sys
import traceback
import pdb

from html.parser import HTMLParser
import xml.etree.ElementTree as ET

print("Running curse")

""" References
  + <https://github.com/ajalt/fuckitpy>
  + <https://www.reddit.com/r/rust/comments/5penft/comment/dcsgk7n/>
  + <
      https://stackoverflow.com/questions/29492895/bare-words-new-keywords-in-python/29492897#29492897
    >
"""

""" Cursed Characters Map
Open Angle       '<' | \u1438  | "ᐸ"
Close Angle      '>' | \u1433  | "ᐳ"
Space            ' ' | \u3164  | "ㅤ"
Forward Slash    '/' | \u10915 | "𐤕"
Equals Sign      '=' | \uA60C  | "ꘌ"
Quote            '"' | \u05F2  | "ײ"

ᐸpᐳ
ㅤㅤᐸspanᐳHelloㅤWorldᐸ𐤕spanᐳ
ᐸ𐤕pᐳ
"""

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

class Parser(HTMLParser):
    """ Build an HTML Parse Tree """

    def __init__(self):
        super().__init__()
        self.tree = ET.Element("document")
        self.stack = []
    
    @property
    def complete(self):
        """ Check whether the parse tree is complete """
        return len(self.stack) == 0

    def handle_starttag(self, tag, attrs):
        """ Handle start tags """
        element = ET.Element(tag)
        for attr in attrs:
            element.set(attr[0], attr[1])
        self.stack.append(element)
    
    def handle_endtag(self, tag):
        """ Handle end tags """
        try:
            element = self.stack.pop()
        except IndexError:
            raise Exception(f"Unmatched end tag: {tag}")
        if element.tag != tag:
            raise Exception(f"Expected end tag {element.tag}, got {tag}")
        if len(self.stack) == 0:
            self.tree.append(element)
        else:
            self.stack[-1].append(element)
    
    def handle_data(self, data):
        """ Handle data """
        if len(self.stack) == 0:
            self.tree.text = data
        else:
            self.stack[-1].text = data
    
    def handle_startendtag(self, tag, attrs):
        """ Handle self-closing tags """
        element = ET.Element(tag)
        for attr in attrs:
            element.set(attr[0], attr[1])
        self.stack[-1].append(element)


class ErrorHijacker:
    """
    This class interrcepts errors and replaces so they can be silently
    handled.

    In essence, we're using NameErrors to detect our 'cursed' HTML-like
    syntax and then replacing it with valid Python syntax.
    """

    CHARACTER_MAP = BiDict({
        "\U00001438": "<",
        "\U00001433": ">",
        "\U00003164": " ",
        "\U00010915": "/",
        "\U0000A60C": "=",
        "\U000005F2": '"',
    })
    
    def __init__(self, native_hook):
        self.native_hook = native_hook

    def __call__(self, ex_type, value, trace):
        """
        Called when an exception is raised
        """

        if isinstance(value, NameError):
            # Intercept NameError
            # pdb.set_trace()

            # Extract the dirty file and compile it to an AST
            stack = traceback.extract_tb(trace)
            frame = stack[-1]
            filename = frame.filename
            lineno = frame.lineno
            code = ""
            with open(filename, "r") as f:
                raw_lines = f.readlines()
                cleaned_lines = list(self._clean_lines(raw_lines))
                code = "".join(cleaned_lines)
                print(code)
            # Now we have the fixed code, we can compile it and execute it
            exec(compile(code, filename, "exec"))
            return

        self.native_hook(ex_type, value, trace)
    
    def _clean_lines(self, lines):
        """
        Replaces (potentially) cursed characters with correct
        python code
        """
        grab_pattern = re.compile(r"\U00003164*(\U00001438.+\U00001433)")
        parser = None
        prechars = ""
        for line in lines:
            if self.CHARACTER_MAP.keys() & line and grab_pattern.search(line):
                content = line[line.find("\U00001438"):]
                html_content = map_string(content, self.CHARACTER_MAP)
                evaluated_content = self._eval_expressions(html_content)
                if parser is None:
                    prechars = line[:line.find("\U00001438")]
                    parser = Parser()
                parser.feed(evaluated_content)
            if parser is None:
                yield line
            elif parser.complete:
                yield prechars + self._build_code(parser.tree)
                parser = None
                prechars = ""
    
    def _eval_expressions(self, line):
        """
        Evaluates expressions in a line of code in the current
        namespace

        Expressions are marked with an open parenthesis, then a python
        expression that evaluates to a string or value, then a close parenthesis
        and a comma.

        Example: `(1 + 1),`
        """
        pattern = re.compile(r"\((.+?)\),")
        return pattern.sub(lambda m: str(eval(m.group(1))), line)

    def _build_code(self, element_tree):
        """
        Builds a string of python code from an element tree
        """
        xmlstr = ET.tostring(element_tree, encoding="unicode")
        oneline = xmlstr.replace("\n", "")
        return f"\"{oneline}\"\n"
        """
        if element_tree.tag == "document":
            return "HTMLBuilder()." + "".join(self._build_code(e) for e in element_tree)
        code = ""
        for child in element_tree:
            code += f"{child.tag}("
            for attr in child.attrib:
                code += f"{attr}={child.attrib[attr]},"
            if child.text is not None:
                code += f"text=\"{child.text}\""
            code += ")"
            code += f".{self._build_code(child)}"
        return code
        """


class HTMLBuilder:
    """ Function-chaining HTML builder; this is what the HTML syntax targets """

    def __init__(self):
        self._tag = None
        self._text = None
        self._attrib = {}
        self._children = []

handler = ErrorHijacker(sys.excepthook)
sys.excepthook = handler

g = "Test string!"
k = ᐸdivᐳ
ㅤㅤㅤㅤㅤᐸpᐳSomeㅤ(2 + 2),ㅤTextㅤandㅤgㅤisㅤ(g),ᐸ𐤕pᐳ
ᐸ𐤕divᐳ
print(f"k val: \"{k}\"")
