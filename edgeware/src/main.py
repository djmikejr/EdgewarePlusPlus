import logging
import sys
from tkinter import Tk

from features.caption_popup import CaptionPopup
from features.image_popup import ImagePopup
from features.misc import handle_discord, handle_wallpaper, make_tray_icon, open_web, play_audio
from features.prompt import Prompt
from features.startup_splash import StartupSplash
from features.video_popup import VideoPopup
from utils import utils
from utils.pack import Pack
from utils.settings import Settings


def main(root: Tk, settings: Settings, pack: Pack) -> None:
    if utils.roll(settings.audio_chance):
        play_audio(settings, pack)

    if utils.roll(settings.video_chance):
        VideoPopup(root, settings, pack)

    if utils.roll(settings.image_chance):
        ImagePopup(root, settings, pack)

    if utils.roll(settings.caption_popup_chance):
        CaptionPopup(settings, pack)

    if utils.roll(settings.prompt_chance):
        Prompt(settings, pack)

    if utils.roll(settings.web_chance):
        open_web(pack)

    root.after(settings.delay, lambda: main(root, settings, pack))


if __name__ == "__main__":
    root = Tk()
    settings = Settings()
    pack = Pack()

    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    def start_main() -> None:
        make_tray_icon(root, settings, pack)
        handle_wallpaper(root, settings, pack)
        handle_discord(root, settings, pack)
        root.after(0, main(root, settings, pack))

    if settings.startup_splash:
        root.after(0, lambda: StartupSplash(pack, start_main))
    else:
        root.after(0, start_main)

    root.withdraw()
    root.mainloop()
