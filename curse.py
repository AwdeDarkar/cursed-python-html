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
                #print(code)
            # Now we have the fixed code, we can compile it and execute it
            exec(compile(code, filename, "exec"))
            return

        self.native_hook(ex_type, value, trace)
    
    def _clean_lines(self, lines):
        """
        Replaces (potentially) cursed characters with correct
        python code
        """
        grab_pattern = re.compile(r"\U00003164*(\U00001438[\w\U00003164]+\U00001433)")
        for line in lines:
            if self.CHARACTER_MAP.keys() & line:
                line = grab_pattern.sub(self._replace, line)
            yield line
    
    def _replace(self, match):
        """
        Replaces cursed characters with parsed HTML
        """
        html_string = map_string(match.group(1), self.CHARACTER_MAP)
        pass


handler = ErrorHijacker(sys.excepthook)
sys.excepthook = handler

k = ᐸblahㅤz=33ᐳ
print(f"k val: \"{k}\"")
