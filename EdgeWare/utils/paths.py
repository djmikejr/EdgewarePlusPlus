import os
from dataclasses import dataclass
from pathlib import Path

PATH = Path(__file__).parent.parent

@dataclass
class Process:
    DISCORD = PATH / 'discord_handler.pyw'
    POPUP = PATH / 'popup.pyw'
    PROMPT = PATH / 'prompt.pyw'
    STARTUP = PATH / 'startup_flair.pyw'
    SUBLABEL = PATH / 'sublabel.pyw'

@dataclass
class Resource:
    ROOT = PATH / 'resource'

    # Directories
    AUDIO = ROOT / 'aud'
    IMAGE = ROOT / 'img'
    SUBLIMINALS = ROOT / 'subliminals'
    VIDEO = ROOT / 'vid'

    # Files
    CAPTIONS = ROOT / 'captions.json'
    CONFIG = ROOT / 'config.json'
    CORRUPTION = ROOT / 'corruption.json'
    DISCORD = ROOT / 'discord.dat'
    ICON = ROOT / 'icon.ico'
    INFO = ROOT / 'info.json'
    SPLASH = None
    MEDIA = ROOT / 'media.json'
    PROMPT = ROOT / 'prompt.json'
    WALLPAPER = ROOT / 'wallpaper.png'
    WEB = ROOT / 'web.json'
    WEB_RESOURCE = ROOT / 'webResource.json'

for file_format in ['png', 'gif', 'jpg', 'jpeg', 'bmp']:
    path = Resource.ROOT / f'loading_splash.{file_format}'
    if os.path.isfile(path):
        Resource.SPLASH = path
        break
