from dataclasses import dataclass, astuple


@dataclass
class Dimension:
    width: int
    height: int

    def __iter__(self):
        yield from astuple(self)

    def astuple(self):
        return astuple(self)


@dataclass(frozen=True)
class Cell:
    x: int
    y: int

    def __iter__(self):
        yield from astuple(self)


Grid = set[Cell]


@dataclass
class Neighbors:
    dead: Grid
    alive: Grid

    def __iter__(self):
        yield from astuple(self)


@dataclass
class Board:
    dim: Dimension
    grid: Grid
