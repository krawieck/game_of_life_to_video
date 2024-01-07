from collections import defaultdict
from copy import deepcopy
from typing import Optional
from functools import partial

from definitions import Neighbors, Cell, Grid, Dimension
from constants import FRAME_LIMIT


def execute_full_game(initial_grid: Grid, *, frame_limit: Optional[int] = None,
                      dimensions: Dimension) -> list[Grid]:
    current_grid = initial_grid
    all_grids = [initial_grid]
    frame_number = 0

    while True:
        new_grid = next_round(current_grid)

        # limit grid size
        new_grid = set(filter(partial(within_dimensions, dimensions), new_grid))
        # else:
        # max_dif_x = max(new_grid, )
        # what if sth goes ridiculoslousy far?

        # limit frames
        if frame_limit is None and new_grid in all_grids:
            break
        if frame_limit is not None and frame_limit <= frame_number:
            break
        if frame_number >= FRAME_LIMIT:
            break

        all_grids.append(new_grid)

    return all_grids


def within_dimensions(dimensions: Dimension, cell: Cell) -> bool:
    width, height = dimensions
    x, y = cell
    return 0 <= x <= width and 0 <= y <= height


def get_neighbors(grid: Grid, x: int, y: int) -> Neighbors:
    offsets = [(-1, -1), (0, -1), (1, -1), (-1, 0),
               (1, 0), (-1, 1), (0, 1), (1, 1)]
    possible_neighbors = {Cell(x + x_add, y + y_add) for x_add, y_add in offsets}
    alive = {Cell(pos.x, pos.y) for pos in possible_neighbors if pos in grid}
    return Neighbors(alive, possible_neighbors - alive)


def next_round(old_grid: Grid) -> Grid:
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


def grid_from_string(string: str) -> Grid:
    """
    converts a string to a Grid. should be formatted like this:
    <x> <y>  <x> <y> ...

    :param string:
    :return:
    """
    return {Cell(int(x), int(y)) for x, y in map(lambda s: s.split(' '), string.split('  '))}
