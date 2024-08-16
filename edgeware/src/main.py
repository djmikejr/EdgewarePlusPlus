import logging
import random
import sys
from collections.abc import Callable
from dataclasses import dataclass
from tkinter import Tk

from features.caption_popup import CaptionPopup
from features.image_popup import ImagePopup
from features.misc import handle_discord, handle_mitosis_mode, handle_timer_mode, handle_wallpaper, make_tray_icon, open_web, play_audio
from features.prompt import Prompt
from features.startup_splash import StartupSplash
from features.video_popup import VideoPopup
from utils import utils
from utils.pack import Pack
from utils.settings import Settings
from utils.utils import State


@dataclass
class RollTarget:
    function: Callable[[], None]
    chance: int

    def roll(self) -> None:
        if utils.roll(self.chance):
            self.function()


def main(root: Tk, settings: Settings, pack: Pack, state: State) -> None:
    targets = [
        RollTarget(lambda: ImagePopup(root, settings, pack, state), settings.image_chance if not settings.mitosis_mode else 0),
        RollTarget(lambda: VideoPopup(root, settings, pack, state), settings.video_chance if not settings.mitosis_mode else 0),
        RollTarget(lambda: CaptionPopup(settings, pack), settings.caption_popup_chance),
        RollTarget(lambda: Prompt(settings, pack, state), settings.prompt_chance),
        RollTarget(lambda: play_audio(settings, pack, state), settings.audio_chance),
        RollTarget(lambda: open_web(pack), settings.web_chance),
    ]

    if settings.single_mode:
        try:
            function = random.choices(list(map(lambda target: target.function, targets)), list(map(lambda target: target.chance, targets)), k=1)[0]
        except Exception:
            function = targets[0].function  # Exception thrown when all chances are 0
        function()
    else:
        for target in targets:
            target.roll()

    root.after(settings.delay, lambda: main(root, settings, pack, state))


if __name__ == "__main__":
    root = Tk()
    settings = Settings()
    pack = Pack()
    state = State()

    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    def start_main() -> None:
        make_tray_icon(root, settings, pack, state)
        handle_wallpaper(root, settings, pack)
        handle_discord(root, settings, pack)
        handle_timer_mode(root, settings, state)
        handle_mitosis_mode(root, settings, pack, state)
        root.after(0, main(root, settings, pack, state))

    if settings.startup_splash:
        root.after(0, lambda: StartupSplash(pack, start_main))
    else:
        root.after(0, start_main)

    root.withdraw()
    root.mainloop()
