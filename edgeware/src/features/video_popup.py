from tkinter import Tk

from features.popup import Popup
from utils.pack import Pack
from utils.settings import Settings
from videoprops import get_video_properties
from widgets.video_player import VideoPlayer


class VideoPopup(Popup):
    def __init__(self, root: Tk, settings: Settings, pack: Pack):
        super().__init__(root, settings, pack)

        video = pack.random_video()
        properties = get_video_properties(video)

        self.set_size_and_position(properties["width"], properties["height"])
        # TODO: Might be necessary to fix bugs
        # self.wait_visibility(self)
        self.player = VideoPlayer(self, video, (self.width, self.height), self.settings.video_volume, self.settings.vlc_mode)

        self.init_finish()

    def close(self) -> None:
        self.player.on_close()
        super().close()
