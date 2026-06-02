from abc import ABC, abstractmethod
from enum import Enum


class CellStatus(Enum):
    EMPTY = 0
    WALL = 1
    EXIT = 2

class MoveTo(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

class Player(ABC):
    @abstractmethod
    def think(self, x: int, y: int, exit_x: int, exit_y: int, up: CellStatus, down: CellStatus, right: CellStatus, left: CellStatus) -> MoveTo:
        pass