# Reactive Inline HTMLish Syntax for Python
This is an idea I've had for a while and unfortunately it turns out to be possible: JSX for Python!

Right now it targets tkinter but could theoretically be extended to HTML for reactive web apps. I'm
not going to do that because no one should ever actually _use_ this library.

```python
@TkinterTarget.component
class Main(Component):
    def get_initial_state(self):
        return {
            "count": 0,
        }
    
    def render(self):
        color = "#ff0000"

        def increment():
            self.set_state({
                "count": self.state["count"] + 1,
            })

        return ᐸframeᐳ
        ㅤㅤㅤㅤㅤᐸlabelㅤforegroundꘌײ(color),ײᐳSomeㅤ(self.state.count),ㅤTextᐸ𐤕labelᐳ
        ㅤㅤㅤㅤㅤᐸbuttonㅤcommandꘌײ(increment),ײᐳIncrementᐸ𐤕buttonᐳ
        ᐸ𐤕frameᐳ
```

## Running
If you're brave enough, this project can be run locally

```bash
$ git clone git@github.com:AwdeDarkar/cursed-python-html.git
$ cd cursed-python-html
$ python3 ./main.py
```
