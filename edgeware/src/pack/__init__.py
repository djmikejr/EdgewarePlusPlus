import random
from pathlib import Path

from paths import Assets, Resource

from pack.data import CaptionMood
from pack.load import list_media, load_captions, load_discord, load_info, load_media, load_moods, load_prompt, load_web


class Pack:
    def __init__(self):
        # Pack files
        self.captions = load_captions()
        self.discord = load_discord()
        self.info = load_info()
        self.media_moods = load_media()
        self.prompts = load_prompt()
        self.web = load_web()

        # Data files
        self.active_moods = load_moods(self.info.mood_file)

        # Media
        # TODO: Validate file types
        self.images = list_media(Resource.IMAGE, self.media_moods)
        self.videos = list_media(Resource.VIDEO, self.media_moods)
        self.audio = list_media(Resource.AUDIO, self.media_moods)
        self.subliminals = list_media(Resource.SUBLIMINALS)

        # Paths
        self.icon = Resource.ICON if Resource.ICON.is_file() else Assets.DEFAULT_ICON
        self.wallpaper = Resource.WALLPAPER if Resource.WALLPAPER.is_file() else Assets.DEFAULT_WALLPAPER
        splash_paths = [Resource.SPLASH.with_suffix(suffix) for suffix in [".png", ".gif", ".jpg", ".jpeg", ".bmp"]]
        self.startup_splash = next((path for path in splash_paths if path.is_file()), Assets.DEFAULT_STARTUP_SPLASH)

    def filter_media(self, media_list: list[Path]) -> list[Path]:
        return list(filter(lambda media: media.mood is None or media.mood in self.active_moods.media, media_list))

    # TODO: If there are none?
    def random_image(self) -> Path:
        return random.choice(self.filter_media(self.images)).path

    # TODO: If there are none?
    def random_video(self) -> Path:
        return random.choice(self.filter_media(self.videos)).path

    # TODO: If there are none?
    def random_audio(self) -> Path:
        return random.choice(self.filter_media(self.audio)).path

    def random_subliminal(self) -> Path:
        if len(self.subliminals) > 0:
            return random.choice(self.subliminals).path
        return Assets.DEFAULT_SUBLIMINAL

    def filter_captions(self) -> list[CaptionMood]:
        return list(filter(lambda c: c.mood in self.active_moods.captions, self.captions.moods))

    # TODO: If there are none?
    # TODO: Unused
    def random_caption_for_media(self, media: Path) -> tuple[str, int]:
        moods = self.filter_captions()
        for c in moods:
            if media.name.startswith(c.mood):
                return (random.choice(c.captions), random.randint(1, c.max_clicks))
        return (random.choice(self.captions.default), 1)

    # TODO: If there are none?
    def random_caption(self) -> str:
        moods = [self.captions.default] + list(map(lambda c: c.captions, self.filter_captions()))
        return random.choice([caption for mood in moods for caption in mood])

    def random_denial(self) -> str:
        return random.choice(self.captions.denial)  # Guaranteed to be non-empty

    # TODO: If there are none?
    def random_prompt(self) -> str:
        moods = list(filter(lambda p: p.mood in self.active_moods.prompts, self.prompts.moods))
        mood = random.choices(moods, list(map(lambda p: p.weight, moods)), k=1)[0]
        length = random.randint(self.prompts.min_length, self.prompts.max_length)

        prompt = ""
        for n in range(length):
            prompt += random.choice(mood.prompts) + " "

        return prompt.strip()

    # TODO: If there are none?
    def random_web(self) -> str:
        web = random.choice(list(filter(lambda w: w.mood in self.active_moods.web, self.web)))
        return web.url + random.choice(web.args)
