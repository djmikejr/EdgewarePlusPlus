from tkinter import Button, Label, Text, Toplevel

from screeninfo import get_monitors
from utils.pack import Pack
from utils.settings import Settings


class Prompt(Toplevel):
    def __init__(self, settings: Settings, pack: Pack):
        global prompt_active
        if "prompt_active" not in globals():
            prompt_active = False

        if prompt_active:
            return

        prompt_active = True
        super().__init__()

        self.wm_attributes("-topmost", True)
        self.wm_attributes("-type", "splash")

        monitor = next(m for m in get_monitors() if m.is_primary)
        width = monitor.width // 4
        height = monitor.height // 2
        x = monitor.x + (monitor.width - width) // 2
        y = monitor.y + (monitor.height - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")

        Label(self, text="\n" + pack.prompt_command_text + "\n").pack()

        prompt = pack.random_prompt()
        Label(self, text=prompt, wraplength=width).pack()

        input = Text(self)
        input.pack()
        button = Button(self, text=pack.prompt_submit_text, command=lambda: self.submit(settings.prompt_max_mistakes, prompt, input.get(1.0, "end-1c")))
        button.place(x=-10, y=-10, relx=1, rely=1, anchor="se")

    # Checks that the number of mistakes is at most max_mistakes and if so,
    # closes the prompt window. The number of mistakes is computed as the edit
    # (Levenshtein) distance between a and b.
    # https://en.wikipedia.org/wiki/Levenshtein_distance
    def submit(self, max_mistakes: int, a: str, b: str) -> None:
        global prompt_active
        d = [[j for j in range(0, len(b) + 1)]] + [[i] for i in range(1, len(a) + 1)]

        for j in range(1, len(b) + 1):
            for i in range(1, len(a) + 1):
                d[i].append(
                    min(
                        d[i - 1][j] + 1,
                        d[i][j - 1] + 1,
                        d[i - 1][j - 1] + (0 if a[i - 1] == b[j - 1] else 1)
                    )
                )  # fmt: skip

        if d[len(a)][len(b)] <= max_mistakes:
            self.destroy()
            prompt_active = False
