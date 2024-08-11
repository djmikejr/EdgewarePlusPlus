from tkinter import Tk

from features.popup import Popup
from utils.pack import Pack
from utils.settings import Settings
from videoprops import get_video_properties
from widgets.video_player import VideoPlayer


class VideoPopup(Popup):
    def __init__(self, root: Tk, settings: Settings, pack: Pack):
        if not self.should_init(settings):
            return
        super().__init__(root, settings, pack)

        video = pack.random_video()
        properties = get_video_properties(video)

        self.set_size_and_position(properties["width"], properties["height"])
        # TODO: Might be necessary to fix bugs
        # self.wait_visibility(self)
        self.player = VideoPlayer(self, video, (self.width, self.height), self.settings.video_volume, self.settings.vlc_mode)

        self.init_finish()

    def should_init(self, settings: Settings) -> bool:
        global video_number
        if "video_number" not in globals():
            video_number = 0

        if video_number < settings.max_video:
            video_number += 1
            return True
        return False

    def close(self) -> None:
        global video_number

        self.player.on_close()
        super().close()
        video_number -= 1
