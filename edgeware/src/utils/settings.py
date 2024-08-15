import ast
import json
import os
import shutil

from utils.paths import Assets, Data


class Settings:
    def __init__(self):
        if not os.path.exists(Data.CONFIG):
            Data.ROOT.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(Assets.DEFAULT_CONFIG, Data.CONFIG)

        with open(Data.CONFIG) as f:
            config = json.loads(f.read())

        # General
        self.theme = config["themeType"]
        self.startup_splash = bool(config["showLoadingFlair"])
        self.panic_disabled = bool(config["panicDisabled"])
        self.panic_key = config["panicButton"]

        # Popups
        self.delay = int(config["delay"])  # Milliseconds
        self.image_chance = int(config["popupMod"])  # 0 to 100
        self.opacity = int(config["lkScaling"]) / 100  # Float between 0 and 1
        self.timeout_enabled = bool(config["timeoutPopups"])
        self.timeout = int(config["popupTimeout"]) * 1000  # Milliseconds
        self.buttonless = bool(config["buttonless"])

        # Overlays
        self.denial_chance = int(config["denialChance"]) if bool(config["denialMode"]) else 0  # 0 to 100
        self.subliminal_chance = int(config["subliminalsChance"]) if bool(config["popupSubliminals"]) else 0  # 0 to 100
        self.max_subliminals = int(config["maxSubliminals"])
        self.subliminal_opacity = int(config["subliminalsAlpha"]) / 100  # Float between 0 and 1

        # Web
        self.web_chance = int(config["webMod"])  # 0 to 100
        self.web_on_popup_close = bool(config["webPopup"])

        # Prompt
        self.prompt_chance = int(config["promptMod"])  # 0 to 1000
        self.prompt_max_mistakes = int(config["promptMistakes"])

        # Audio
        self.audio_chance = int(config["audioMod"])  # 0 to 100
        self.max_audio = int(config["maxAudio"]) if bool(config["maxAudioBool"]) else float("inf")

        # Video
        self.video_chance = int(config["vidMod"])  # 0 to 100
        self.video_volume = int(config["videoVolume"])  # 0 to 100
        self.max_video = int(config["maxVideos"]) if bool(config["maxVideoBool"]) else float("inf")
        self.vlc_mode = bool(config["vlcMode"])

        # Captions
        self.captions_in_popups = bool(config["showCaptions"])
        self.caption_popup_chance = int(config["capPopChance"])  # 0 to 100
        self.caption_popup_opacity = int(config["capPopOpacity"]) / 100  # Float between 0 and 1
        self.caption_popup_timeout = int(config["capPopTimer"])  # Milliseconds

        # Wallpaper
        self.rotate_wallpaper = bool(config["rotateWallpaper"])
        self.wallpaper_timer = int(config["wallpaperTimer"]) * 1000  # Milliseconds
        self.wallpaper_variance = int(config["wallpaperVariance"]) * 1000  # Milliseconds
        self.wallpapers = list(ast.literal_eval(config["wallpaperDat"]).values())

        # Dangerous
        self.show_on_discord = bool(config["showDiscord"])

        # Basic modes
        self.moving_chance = int(config["movingChance"])  # 0 to 100
        self.moving_speed = int(config["movingSpeed"])
        self.moving_random = bool(config["movingRandom"])

        # Dangerous modes
        self.timer_mode = bool(config["timerMode"])
        self.timer_time = int(config["timerSetupTime"]) * 60 * 1000  # Milliseconds
        self.mitosis_mode = bool(config["mitosisMode"])
        self.mitosis_strength = int(config["mitosisStrength"])
