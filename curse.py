import re
import sys
import traceback
import pdb

from types import SimpleNamespace
from html.parser import HTMLParser

from utils import BiDict, map_string, HTMLBuilder

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
class Parser(HTMLParser):
    """ Build an HTML Parse Tree """

    def __init__(self):
        super().__init__()
        self.code = ""
        self.stack = []
    
    @property
    def complete(self):
        """ Check whether the parse tree is complete """
        return len(self.stack) == 0 and self.code != ""
    
    @property
    def top(self):
        """ Get the top (latest) element of the stack """
        return self.stack[-1]

    def handle_starttag(self, tag, attrs):
        """ Handle start tags """
        print(f"Start tag: {tag}, current stack: {self.stack}")
        self.code += f".tag(\"{tag}\""
        for aname, aval in attrs:
            self.code += f", {aname}=\"{aval or True}\""
        self.stack.append(tag)
        self.code += ")"
    
    def handle_endtag(self, tag):
        """ Handle end tags """
        print(f"End tag: {tag}, current stack: {self.stack}")
        try:
            prev_tag = self.stack.pop()
            self.code += ".pop()"
        except IndexError:
            raise Exception(f"Unmatched end tag: {tag}")
        if prev_tag != tag:
            raise Exception(f"Expected end tag {prev_tag}, got {tag}")
    
    def handle_data(self, data):
        """ Handle data """
        if data.strip() == "":
            return
        self.code += f".text(\"{data.strip()}\")"
    
    def handle_startendtag(self, tag, attrs):
        """ Handle self-closing tags """
        self.code += f".tag(\"{tag}\""
        for aname, aval in attrs:
            self.code += f", {aname}=\"{aval or True}\""
        self.code += ").pop()"


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
                print("".join([
                    f"{i+lineno:03d} {l}" for i, l in enumerate(cleaned_lines[lineno-5:])
                ]))
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
                # pdb.set_trace()
                code = f"{prechars}HTMLBuilder(){parser.code}\n"
                print(f"Core code: {code}")
                yield code
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


handler = ErrorHijacker(sys.excepthook)
sys.excepthook = handler

g = "Test string!"
k = ᐸdivᐳ
ㅤㅤㅤㅤㅤᐸpᐳSomeㅤ(2 + 2),ㅤTextㅤandㅤgㅤisㅤ(g),ᐸ𐤕pᐳ
ᐸ𐤕divᐳ
print(f"k val: \"{k.to_dict()}\"")
