"""
This module has data structures for ``game_of_life_to_video``. They are based on the ones from [this implementation of
 game of life](https://matgomes.com/conways-game-of-life-python/). The biggest difference is they got changed from
 ``namedtuple``s to ``dataclass``es
"""

from dataclasses import dataclass, astuple


@dataclass
class Dimensions:
    """Represents the dimensions of a grid in the game of life"""
    width: int
    height: int

    def __post_init__(self):
        if self.width < 2 or self.height < 2:
            raise ValueError("the grid can't be smaller than 2x2")

    def __iter__(self):
        yield from astuple(self)

    def astuple(self):
        return astuple(self)


@dataclass(frozen=True)
class Cell:
    """Represents a single cell in the game of life grid"""
    x: int
    y: int

    def __iter__(self):
        yield from astuple(self)


Grid = set[Cell]


@dataclass
class Neighbors:
    """Represents the neighbors of a cell in the Game of Life"""
    dead: Grid
    alive: Grid

    def __iter__(self):
        yield from astuple(self)


@dataclass
class Board:
    """Represents the game board for the Game of Life"""
    dim: Dimensions
    grid: Grid
