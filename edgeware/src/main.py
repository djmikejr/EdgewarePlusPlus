import logging
import sys
from tkinter import Tk

from features.caption_popup import CaptionPopup
from features.hibernate import main_hibernate
from features.image_popup import ImagePopup
from features.misc import handle_discord, handle_mitosis_mode, handle_timer_mode, handle_wallpaper, make_tray_icon, open_web, play_audio
from features.prompt import Prompt
from features.startup_splash import StartupSplash
from features.video_popup import VideoPopup
from pack import Pack
from roll import RollTarget, roll_targets
from settings import Settings
from utils.utils import State


def main(root: Tk, settings: Settings, targets: list[RollTarget]) -> None:
    roll_targets(settings, targets)
    root.after(settings.delay, lambda: main(root, settings, targets))


if __name__ == "__main__":
    root = Tk()
    settings = Settings()
    pack = Pack()
    state = State()

    # TODO: Use a dict?
    targets = [
        RollTarget(lambda: ImagePopup(root, settings, pack, state), settings.image_chance if not settings.mitosis_mode else 0),
        RollTarget(lambda: VideoPopup(root, settings, pack, state), settings.video_chance if not settings.mitosis_mode else 0),
        RollTarget(lambda: CaptionPopup(settings, pack), settings.caption_popup_chance),
        RollTarget(lambda: Prompt(settings, pack, state), settings.prompt_chance),
        RollTarget(lambda: play_audio(settings, pack, state), settings.audio_chance),
        RollTarget(lambda: open_web(pack), settings.web_chance),
    ]

    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    def start_main() -> None:
        make_tray_icon(root, settings, pack, state, lambda: main_hibernate(root, settings, pack, state, targets))
        handle_discord(root, settings, pack)
        handle_timer_mode(root, settings, state)
        handle_mitosis_mode(root, settings, pack, state)

        if not settings.hibernate_fix_wallpaper:
            handle_wallpaper(root, settings, pack, state)

        if settings.hibernate_mode:
            main_hibernate(root, settings, pack, state, targets)
        else:
            main(root, settings, targets)

    if settings.startup_splash:
        root.after(0, lambda: StartupSplash(pack, start_main))
    else:
        root.after(0, start_main)

    root.withdraw()
    root.mainloop()
