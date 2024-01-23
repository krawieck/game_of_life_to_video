from goltv.main import play_game_and_render_it, DimensionsClickType, cli
from goltv.converters import board_from_string, grid_from_string
from goltv.constants import (FRAME_EXT, MAX_RES, DEAD_SHADE, ALIVE_SHADE, AUTO_FRAMERATE_THRESHOLDS,
                             FRAME_LIMIT, AUTO_FRAMERATE_FALLBACK, OUTPUT_EXTS)
from goltv.definitions import Board, Dimensions, Grid, Cell, Neighbors
from goltv.game_of_life import execute_full_game
from goltv.renderer import write_frames, render_frames


"""
# Game Of Life to video

![Project banner](../assets/banner.png)

This is a project dedicated to executing a game of life and creating a video out of it.
It can be used both as a command line tool and as a library.
"""
