from tkinter import Tk

from features.popup import Popup
from utils.pack import Pack
from utils.settings import Settings
from utils.utils import State
from videoprops import get_video_properties
from widgets.video_player import VideoPlayer


class VideoPopup(Popup):
    def __init__(self, root: Tk, settings: Settings, pack: Pack, state: State):
        if not self.should_init(settings, state):
            return
        super().__init__(root, settings, pack, state)

        video = pack.random_video()
        properties = get_video_properties(video)

        self.set_size_and_position(properties["width"], properties["height"])
        # TODO: Might be necessary to fix bugs
        # self.wait_visibility(self)
        self.player = VideoPlayer(self, video, (self.width, self.height), self.settings.video_volume, self.settings.vlc_mode)

        self.init_finish()

    def should_init(self, settings: Settings, state: State) -> bool:
        if state.video_number < settings.max_video:
            state.video_number += 1
            return True
        return False

    def close(self) -> None:
        self.player.on_close()
        super().close()
        self.state.video_number -= 1
