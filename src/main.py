from tempfile import TemporaryDirectory

from game import execute_full_game, grid_from_string
from definitions import Board, Dimension
from renderer import render_video

example_grid = "1 1  2 1  3 1"


def play_game_and_render_it(board: Board):
    game_states = execute_full_game(board.grid, dimensions=board.dim)
    with TemporaryDirectory() as tmp_dir:
        render_video(game_states, tmp_dir, dimension=board.dim)


def main():
    board = Board(Dimension(10, 10), grid_from_string(example_grid))

    play_game_and_render_it(board)


if __name__ == '__main__':
    main()
