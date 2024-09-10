from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any


@dataclass
class Subject:
    value: Any
    observers: list[Callable[[], None]] = field(default_factory=list)

    def notify(self) -> None:
        for observer in self.observers:
            observer()

    def attach(self, observer: Callable[[], None]) -> None:
        self.observers.append(observer)


# TODO: Check if there are other uses for observers
@dataclass
class State:
    audio_number = 0
    fill_number = 0
    _popup_number = Subject(0)
    prompt_active = False
    subliminal_number = 0
    video_number = 0

    timer_active = False

    hibernate_active = False
    hibernate_id = None
    pump_scare = False

    corruption_level = 1

    gallery_dl_process = None

    @property
    def popup_number(self) -> int:
        return self._popup_number.value

    @popup_number.setter
    def popup_number(self, value: int) -> None:
        self._popup_number.value = value
        self._popup_number.notify()

    def reset_wallpaper(self) -> bool:
        return not self.hibernate_active and self.popup_number == 0
