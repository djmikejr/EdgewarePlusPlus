import time
from itertools import cycle
from pathlib import Path
from threading import Thread
from tkinter import Label, Canvas, TclError, Toplevel

import imageio
from PIL import Image, ImageTk
from utils import utils
from pyvidplayer2 import VideoTkinter

try:
    import vlc
except FileNotFoundError:
    pass


class VideoPlayer:
    def __init__(self, master: Toplevel, video: Path, size: tuple[int, int], volume: int, vlc_mode: bool):
        self.vlc_mode = vlc_mode
        if self.vlc_mode:
            # Max repeat value. This is hacky but seems to be the easiest way to loop the video.
            self.player = vlc.Instance("--input-repeat=65535").media_player_new()
            utils.set_vlc_window(self.player, master.winfo_id())
            self.player.video_set_mouse_input(False)
            self.player.video_set_key_input(False)
            self.player.audio_set_volume(volume)
            self.player.set_media(vlc.Media(video))
            self.player.play()
        else:
            self.canvas = Canvas(master, width=size[0], height=size[1], highlightthickness=0)
            self.canvas.pack()

            self.video = video
            self.player = VideoTkinter(video)
            self.player.resize(size)
            self.player.set_volume(float(volume / 100))

            self.restart = False
            self.animate()

    def animate(self) -> None:
        if self.player.draw(self.canvas, (self.player.current_size[0] / 2, self.player.current_size[1] / 2), force_draw=False):
            self.restart = True  # The draw method can return False before the first frame is drawn
        elif self.restart:
            self.player.restart()
            self.restart = False

        self.canvas.after(int(1 / self.player.frame_rate * 1000), self.animate)

    def on_close(self) -> None:
        if self.vlc_mode:
            self.player.stop()
        else:
            self.player.close()
