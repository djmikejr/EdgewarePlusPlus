import random
from collections.abc import Callable
from dataclasses import dataclass

from settings import Settings


@dataclass
class RollTarget:
    function: Callable[[], None]
    chance: int

    def roll(self) -> None:
        if roll(self.chance):
            self.function()


def roll_targets(settings: Settings, targets: list[RollTarget]) -> None:
    if settings.single_mode:
        try:
            function = random.choices(list(map(lambda target: target.function, targets)), list(map(lambda target: target.chance, targets)), k=1)[0]
        except ValueError:
            function = targets[0].function  # Exception thrown when all chances are 0
        function()
    else:
        for target in targets:
            target.roll()


def roll(chance: int) -> bool:
    return random.randint(1, 100) <= chance
