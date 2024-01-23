"""
test
"""
import os
from pathlib import Path
from tempfile import TemporaryDirectory
from datetime import datetime
from typing import Optional

from goltv.constants import OUTPUT_EXTS
from goltv.converters import board_from_string
from goltv.game_of_life import execute_full_game
from goltv.definitions import Board, Dimensions
from goltv.renderer import write_frames, render_frames, assume_framerate

import click


def play_game_and_render_it(board: Board,
                            output_file: Optional[str | Path] = None,
                            framerate: Optional[int] = None,
                            scale_factor: Optional[int] = None) -> None:
    """
    Play the game of life and render it into a video.

    :param board: Initial state of the board.
    :param output_file: Output file path for the rendered video.
    :param framerate: Framerate for the rendered video.
    :param scale_factor: Factor by which the board will be scaled to make the video pleasant to watch.
     By default, it's automatically determined.
    :return: None
    """
    game_states = execute_full_game(board.grid, dimensions=board.dim)
    with TemporaryDirectory() as tmp_dir:
        if output_file is None:
            now = datetime.now()
            output_file = f"{now:%Y}{now:%m}{now:%d}_{now:%H}{now:%M}{now:%S}{OUTPUT_EXTS[0]}"
        if framerate is None:
            framerate = assume_framerate(len(game_states))

        write_frames(game_states, frames_dir=tmp_dir, dimensions=board.dim, scale_factor=scale_factor)
        render_frames(frames_dir=tmp_dir, output_file=output_file, framerate=framerate)


class DimensionsClickType(click.ParamType):
    """
    Custom Click type for handling dimensions input in the format NUMBERxNUMBER.
    """
    name = "dimensions"

    def convert(self, value, param, ctx):
        def nope(e: Optional[ValueError] = None):
            error = "Dimensions need to have a format NUMBERxNUMBER. e.g.: 120x140."
            if e is not None:
                error += f"\nAlso the error message is this: {e}"
            return self.fail(error)

        if value is None:
            return None
        if not isinstance(value, str):
            return nope()

        try:
            width, height = value.split("x")
            return Dimensions(int(width), int(height))
        except ValueError as e:
            return nope(e)


@click.command("game_of_life_to_video")
@click.argument("board_file", type=click.Path(exists=True, dir_okay=False, readable=True))
@click.option("--output", default=None,
              type=click.Path(exists=False, file_okay=True, dir_okay=False, writable=True, readable=False))
@click.option("--dimensions", default=None, type=DimensionsClickType(),
              help="Dimensions for the board, by default get inferred from the input board")
@click.option("--framerate", default=None, type=int,
              help="Dimensions for the board, by default get inferred from the input board")
@click.option("--scale-factor", default=None, type=int,
              help="Factor by which the board will be scaled to make video pleasant to watch. "
                   "By default it's automatically determined")
def cli(board_file: str | Path,
        output: Optional[str | Path],
        dimensions: Optional[Dimensions],
        framerate: Optional[int],
        scale_factor: Optional[int]):
    with open(board_file) as f:
        text_board = f.read()
    try:
        board = board_from_string(text_board)
    except ValueError as e:
        print(f"Error: {e}")
        return 1

    if dimensions is not None:
        board.dim = dimensions
    play_game_and_render_it(board,
                            output,
                            framerate=framerate,
                            scale_factor=scale_factor)


if __name__ == '__main__':
    cli()
