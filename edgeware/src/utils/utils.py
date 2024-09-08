import logging
import platform
import sys
import time

from paths import Data


def init_logging(filename: str) -> str:
    Data.LOGS.mkdir(parents=True, exist_ok=True)
    log_time = time.asctime().replace(" ", "_").replace(":", "-")
    log_file = f"{log_time}-{filename}.txt"

    handlers = [logging.StreamHandler(stream=sys.stdout), logging.FileHandler(filename=Data.LOGS / log_file)]
    logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO, force=True, handlers=handlers)

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
