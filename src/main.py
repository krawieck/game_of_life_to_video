import os
from tempfile import TemporaryDirectory
import re
from time import time
from typing import Optional

from game import execute_full_game, grid_from_string
from definitions import Board, Dimensions
from renderer import write_frames, render_frames, assume_framerate

import click

example_grid = "1 1  2 1  3 1"
pentomino = "50 50  50 51  51 50  51 49  52 50"
testing = "1 1  2 2  3 3  4 4"

examples = [
    ("5 5  5 6  5 7  6 6", (20, 20))
]


def play_game_and_render_it(board: Board, dimensions: Dimensions, framerate: Optional[int]):
    game_states = execute_full_game(board.grid, dimensions=board.dim)
    with TemporaryDirectory() as tmp_dir:
        write_frames(game_states, frames_dir=tmp_dir, dimension=board.dim)
        framerate = assume_framerate(len(game_states))
        render_frames(frames_dir=tmp_dir, framerate=framerate)


class DimensionsClickType(click.ParamType):
    name = "dimensions"

    def convert(self, value, param, ctx):
        def nope():
            return self.fail("Dimensions need to have a format NUMBERxNUMBER. e.g.: 120x140")

        if value is None:
            return None
        if not isinstance(value, str):
            return nope()

        try:
            width, height = value.split("x")
            return Dimensions(int(width), int(height))
        except ValueError:
            return nope()


@click.command()
@click.argument("base_board", type=click.File("rb"))
@click.option("--dimensions", default=None, type=DimensionsClickType(),
              help="Dimensions for the board, by default get inferred from the input board")
@click.option("--scale-factor", default=None, type=int,
              help="Factor by which the board will be scaled to make video pleasant to watch. "
                   "By default it's automatically determined")
def main(base_board: click.File, dimensions: Dimensions, scale_factor: int):
    board = Board(Dimensions(10, 10), grid_from_string(example_grid))
    board = Board(Dimensions(100, 100), grid_from_string(pentomino))
    board = Board(Dimensions(20, 20), grid_from_string(testing))

    # grid, dimensions = examples[0]
    # board = Board(Dimensions(*dimensions), grid_from_string(grid))

    print(base_board)
    print(dimensions)
    print(scale_factor)
    # play_game_and_render_it(board)


if __name__ == '__main__':
    main()
