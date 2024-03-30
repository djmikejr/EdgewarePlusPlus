import ctypes
import os
import pathlib
from pathlib import Path
from utils import utils
from utils.paths import Data, Defaults

# Checking timer
try:
    utils.show_file(Data.HID_TIME)
except:
    ''
if os.path.exists(Data.HID_TIME):
    utils.hide_file(Data.HID_TIME)
    # Do nothing if timer is present
else:
    # Continue if no timer
    utils.set_wallpaper(Defaults.PANIC_WALLPAPER)
    utils.panic_script()
