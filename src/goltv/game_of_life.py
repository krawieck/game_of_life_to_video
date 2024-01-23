"""
This module has everything related to executing the pure game of life. It is heavily based on
[this implementation](https://matgomes.com/conways-game-of-life-python/).

The modifications are as such:
* some names of variables are different
* functions were added
    * ``execute_full_game``
    * ``within_dimensions``

Other modifications in [``definitions``](definitions)
"""

from collections import defaultdict
from copy import deepcopy
from typing import Optional
from functools import partial

from goltv.definitions import Neighbors, Cell, Grid, Dimensions
from goltv.constants import FRAME_LIMIT

import re


def execute_full_game(initial_grid: Grid, *, frame_limit: Optional[int] = None,
                      dimensions: Dimensions) -> list[Grid]:
    """
    Executes a full game of life. Stops only if the ``frame_limit`` has been reached or the grid starts repeating.

    :param initial_grid: Starting state
    :param frame_limit: Limits the number of iterations that the game will go on
    :param dimensions: Dimensions of the grid on which the game will be executed
    :return: A list of all the subsequent iterations of the game of life.
    """
    current_grid = initial_grid
    all_grids = [initial_grid]
    frame_number = 0

    while True:
        new_grid = next_round(current_grid)

        # limit grid size
        new_grid = set(filter(partial(within_dimensions, dimensions), new_grid))

        # limit frames
        if frame_limit is None and new_grid in all_grids or frame_number >= FRAME_LIMIT:
            break
        if frame_limit is not None and frame_limit <= frame_number:
            break

        frame_number += 1
        current_grid = new_grid
        all_grids.append(new_grid)

    return all_grids


def within_dimensions(dimensions: Dimensions, cell: Cell) -> bool:
    """
    Helper function that determines if a ``cell`` is within ``dimensions``
    :param dimensions:
    :param cell:
    :return: True if the cell is within the dimensions, False otherwise
    """
    width, height = dimensions
    x, y = cell
    return 0 <= x < width and 0 <= y < height


def get_neighbors(grid: Grid, x: int, y: int) -> Neighbors:
    """
    Get the alive and dead neighbors of a cell in the grid.

    :param grid: The current state of the grid
    :param x: X-coordinate of the cell
    :param y: Y-coordinate of the cell
    :return: Neighbors object with dead and alive neighbors
    """
    offsets = [(-1, -1), (0, -1), (1, -1), (-1, 0),
               (1, 0), (-1, 1), (0, 1), (1, 1)]
    possible_neighbors = {Cell(x + x_add, y + y_add) for x_add, y_add in offsets}
    alive = {Cell(pos.x, pos.y) for pos in possible_neighbors if pos in grid}
    return Neighbors(alive, possible_neighbors - alive)


def next_round(old_grid: Grid) -> Grid:
    """
    Compute the next iteration of the game of life based on the provided grid.

    :param old_grid: The current state of the grid
    :return: The next state of the grid
    """
    new_grid = deepcopy(old_grid)
    may_be_resurected = defaultdict(int)

    for cell in old_grid:
        x, y = cell
        alive_neighbors, dead_neighbors = get_neighbors(old_grid, x, y)

        if len(alive_neighbors) not in [2, 3]:
            new_grid.remove(cell)

        for dead_cell in dead_neighbors:
            may_be_resurected[dead_cell] += 1

    for position, _ in filter(lambda item: item[1] == 3, may_be_resurected.items()):
        new_grid.add(position)

    return new_grid

