import logging
import sys
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


def main(root: Tk, settings: Settings, pack: Pack, state: State) -> None:
    if utils.roll(settings.audio_chance):
        play_audio(settings, pack, state)

    if not settings.mitosis_mode and utils.roll(settings.video_chance):
        VideoPopup(root, settings, pack, state)

    if not settings.mitosis_mode and utils.roll(settings.image_chance):
        ImagePopup(root, settings, pack, state)

    if utils.roll(settings.caption_popup_chance):
        CaptionPopup(settings, pack)

    if utils.roll(settings.prompt_chance):
        Prompt(settings, pack, state)

    if utils.roll(settings.web_chance):
        open_web(pack)

    root.after(settings.delay, lambda: main(root, settings, pack, state))


if __name__ == "__main__":
    root = Tk()
    settings = Settings()
    pack = Pack()
    state = State()

    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    def start_main() -> None:
        make_tray_icon(root, settings, pack)
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
