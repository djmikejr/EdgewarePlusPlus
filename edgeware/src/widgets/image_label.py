from itertools import cycle
from threading import Thread
from tkinter import Label, Toplevel

from PIL import Image, ImageFilter, ImageTk


class GifLike:
    def __init__(self, frames: list[tuple[Image.Image, int]]):
        self.frames = frames
        self.frame = 0
        self.n_frames = len(frames)
        self.update_info()

    def resize(self, size: tuple[int, int], resample: int) -> Image.Image:
        return self.frames[self.frame][0].resize(size, resample)

    def seek(self, frame: int) -> None:
        self.frame = frame
        self.update_info()

    def update_info(self) -> None:
        self.info = {"duration": self.frames[self.frame][1]}


def resize_and_filter(image: Image.Image, size: tuple[int], filter: ImageFilter.Filter | None) -> Image.Image:
    resized = image.resize(size, Image.LANCZOS).convert("RGBA")
    return resized.filter(filter) if filter else resized


class ImageLabel(Label):
    def __init__(self, master: Toplevel, image: Image.Image | GifLike, size: tuple[int], filter: ImageFilter.Filter | None = None):
        super().__init__(master)

        self.image = image
        self.size = size
        self.filter = filter

        if hasattr(self.image, "n_frames") and self.image.n_frames > 1:
            # GIFs are loaded in a thread for performance reasons
            Thread(target=self.init_animation, daemon=True).start()
        else:
            self.photo_image = ImageTk.PhotoImage(resize_and_filter(self.image, self.size, self.filter))
            self.config(image=self.photo_image)

    def init_animation(self) -> None:
        frames = []
        for i in range(self.image.n_frames):
            self.image.seek(i)
            photo_image = ImageTk.PhotoImage(resize_and_filter(self.image, self.size, self.filter))
            frames.append((photo_image, self.image.info["duration"]))
        self.frames = cycle(frames)
        self.animate()

    def animate(self) -> None:
        frame, duration = next(self.frames)
        self.config(image=frame)
        self.after(duration, self.animate)
