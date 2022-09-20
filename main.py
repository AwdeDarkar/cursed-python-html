import curse
from tktarget import TkinterTarget, Component

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

if __name__ == "__main__":
    hack_guard = ᐸnotag𐤕ᐳ # Prevents the window from running twice
    TkinterTarget.main().start()