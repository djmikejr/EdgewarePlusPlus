from threading import Thread
from tkinter import Tk

from features.caption_popup import CaptionPopup
from features.corruption import handle_corruption
from features.drive import fill_drive, replace_images
from features.hibernate import main_hibernate, start_main_hibernate
from features.image_popup import ImagePopup
from features.misc import (
    handle_booru_download,
    handle_discord,
    handle_mitosis_mode,
    handle_timer_mode,
    handle_wallpaper,
    make_desktop_icons,
    make_tray_icon,
    open_web,
    play_audio,
)
from features.prompt import Prompt
from features.startup_splash import StartupSplash
from features.video_popup import VideoPopup
from pack import Pack
from panic import start_panic_listener
from roll import RollTarget, roll_targets
from settings import Settings
from state import State
from utils import utils


def main(root: Tk, settings: Settings, targets: list[RollTarget]) -> None:
    roll_targets(settings, targets)
    Thread(target=lambda: fill_drive(root, settings, pack, state), daemon=True).start()  # Thread for performance reasons
    root.after(settings.delay, lambda: main(root, settings, targets))


if __name__ == "__main__":
    utils.init_logging("main")

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

    def start_main() -> None:
        Thread(target=lambda: replace_images(root, settings, pack), daemon=True).start()  # Thread for performance reasons
        make_tray_icon(root, settings, pack, state, lambda: main_hibernate(root, settings, pack, state, targets))
        make_desktop_icons(settings)
        handle_corruption(root, settings, pack, state)
        handle_booru_download(settings, state)
        handle_discord(root, settings, pack)
        handle_timer_mode(root, settings, state)
        handle_mitosis_mode(root, settings, pack, state)
        start_panic_listener(root, settings, state)

        if settings.hibernate_mode:
            start_main_hibernate(root, settings, pack, state, targets)
        else:
            handle_wallpaper(root, settings, pack, state)
            main(root, settings, targets)

    if settings.startup_splash:
        root.after(0, lambda: StartupSplash(pack, start_main))
    else:
        root.after(0, start_main)

    root.withdraw()
    root.mainloop()
