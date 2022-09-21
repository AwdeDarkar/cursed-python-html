# Native inline HTML syntax for Python
This is an idea I've had for a while and unfortunately it turns out to be possible: JSX for Python.

It works without (explicit) transpilation in pure native python and supports custom components and
state updates.

## Example
Depending on your font, the characters may render strangely. But it's valid python code and that's
all the interpreter cares about!

```python
class Main(Component):
    """
    Demo Application Component

    This app demonstrates the 'cursed' inline html syntax with
    a classic click counter app.
    """

    def get_initial_state(self):
        return {
            "count": 0,
            "color": "#000000",
        }
    
    def render(self):
        def increment():
            self.set_state({
                "count": self.state["count"] + 1,
            })
        
        def pick_color():
            from tkinter import colorchooser
            self.set_state({
                "color": colorchooser.askcolor(title="Pick a color")[1],
            })

        return ᐸframeᐳ
        ㅤㅤㅤㅤㅤᐸlabelㅤforegroundꘌײ(self.state.color),ײᐳCurrentㅤcountㅤisㅤ(self.state.count),ᐸ𐤕labelᐳ
        ㅤㅤㅤㅤㅤᐸbuttonㅤcommandꘌײ(increment),ײᐳIncrementᐸ𐤕buttonᐳ
        ㅤㅤㅤㅤㅤᐸbuttonㅤcommandꘌײ(pick_color),ײᐳChangeㅤtextㅤcolorᐸ𐤕buttonᐳ
        ᐸ𐤕frameᐳ
```

## Running
This project has no third-party dependencies so running it is as simple as cloning and executing the
`main.py` script.

```bash
git clone git@github.com:AwdeDarkar/cursed-python-html.git
cd cursed-python-html
python3 ./main.py
```

## How It Works
Basically there are a few key ideas underlining this demo: weird unicode characters that python
treats as letters but that look like symbols, overriding the `sys.excepthook` to recover from
`NameError`s, and 'in-place' transpiling.

Essentially, the HTMLish syntax looks like tuples of unbound variables to python. When the
interpreter encounters them, it raises a `NameError` that we can detect and use to re-run the
source file with corrected code.

### Limitations
There are a few known problems:
  + State in sub-components is lost when a parent re-renders
  + Custom components must all be in the same file
  + Re-renders unmount and recreate the whole widget tree from parent down, causing occasional
    flashes on updates.
  + The file in which the HTMLish syntax appears is run twice, along with any side-effects

These are bugs that I could fix, but I probably won't because no one should actually _use_ this
for anything and there's really only so much effort I'm willing to invest in this farce.

## Why???
This nightmare of an idea crawled into my head when I read about someone using characters from
the Canadian Aboriginal Syllabics block to [fake generics in
Go](https://old.reddit.com/r/rust/comments/5penft/comment/dcsgk7n/).

Mainly, I did this just to see if I could.
