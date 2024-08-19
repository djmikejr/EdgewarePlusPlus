import platform
from dataclasses import dataclass


@dataclass
class State:
    audio_number = 0
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
