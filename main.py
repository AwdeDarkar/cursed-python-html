import curse
from tktarget import TkinterTarget, Component

@TkinterTarget.component
class Main(Component):
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

if __name__ == "__main__":
    # Prevents the window from running twice
    hack_guard = ᐸnotag𐤕ᐳ
    TkinterTarget.main().start()