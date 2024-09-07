import logging
import platform
import sys
import time
from dataclasses import dataclass

from paths import Data


@dataclass
class State:
    audio_number = 0
    fill_number = 0
    popup_number = 0
    prompt_active = False
    subliminal_number = 0
    video_number = 0

    timer_active = False

    hibernate_active = False
    hibernate_id = None
    pump_scare = False

    def reset_wallpaper(self) -> bool:
        return not self.hibernate_active and self.popup_number == 0


def init_logging(filename: str) -> str:
    Data.LOGS.mkdir(parents=True, exist_ok=True)
    log_time = time.asctime().replace(" ", "_").replace(":", "-")
    log_file = f"{log_time}-{filename}.txt"

    handlers = [logging.StreamHandler(stream=sys.stdout), logging.FileHandler(filename=Data.LOGS / log_file)]
    logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.DEBUG, force=True, handlers=handlers)

    return log_file


def is_linux():
    return platform.system() == "Linux"


def is_windows():
    return platform.system() == "Windows"


def is_mac():
    return platform.system() == "Darwin"


if is_linux():
    from utils.linux import *  # noqa: F403
elif is_windows():
    from utils.windows import *  # noqa: F403
elif is_mac():
    from utils.mac import *  # noqa: F403
else:
    raise RuntimeError(f"Unsupported operating system: {platform.system()}")
