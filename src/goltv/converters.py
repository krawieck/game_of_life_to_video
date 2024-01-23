import re
from typing import Optional

from goltv.definitions import Dimensions, Board, Grid, Cell

_BOARD_FROM_STRING_REGEX = re.compile(r"^[10 ]*$")


def board_from_string(text: str, dimensions: Optional[Dimensions] = None) -> Board:
    """
    Convert a string representation of a game of life board to a Board object.

    :param text: String representation of the game board.
    :param dimensions: Optional dimensions for the board. If None, dimensions are inferred from the input.
    :return: Board object representing the game board.
    :raises ValueError: If the input board doesn't have the proper format (1 - alive, 0 - dead).
    """
    lines = text.split("\n")

    # make sure it's correct format
    ylen = len(lines[0])
    xlen = len(lines)

    for line in lines:
        len_line = len(line)
        if len_line > ylen:
            ylen = len_line
        if _BOARD_FROM_STRING_REGEX.match(line) is None:
            raise ValueError("input board doesn't have the proper format (1 - alive, 0 or space - dead)")

    grid = Grid()
    for i, line in enumerate(lines):
        for j, c in enumerate(line):
            if c == '1':
                grid.add(Cell(i, j))

    if dimensions is None:
        dimensions = Dimensions(xlen, ylen)

    return Board(dimensions, grid)


_GRID_FROM_STRING_REGEX = re.compile(r"^\d+\s\d+((\s\s\d+\s\d+)?)+$")


def grid_from_string(string: str) -> Grid:
    """
    converts a string to a Grid. should be formatted like this:
    <x> <y>  <x> <y> ...

    this is mostly for testing!

    :param string: Formatted string representing cell coordinates
    :return: A Grid
    :raises ValueError: If the input string doesn't have the proper format
    """
    if string == "":
        return Grid()

    if _GRID_FROM_STRING_REGEX.fullmatch(string) is None:
        raise ValueError("doesn't have proper format")

    return {Cell(int(x), int(y)) for x, y in map(lambda s: s.split(' '), string.split('  '))}
