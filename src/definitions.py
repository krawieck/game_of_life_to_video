from dataclasses import dataclass, astuple


@dataclass
class Dimension:
    width: int
    height: int

    def astuple(self):
        return astuple(self)


@dataclass
class Cell:
    x: int
    y: int


Grid = set[Cell]


@dataclass
class Neighbors:
    dead: Grid
    alive: Grid


@dataclass
class Board:
    dim: Dimension
    grid: Grid
