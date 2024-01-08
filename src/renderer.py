from pathlib import Path
from math import floor
import os

import cv2
import numpy as np
import ffmpeg

from definitions import Grid, Dimensions
from constants import FRAME_EXT, MAX_RES, DEAD_SHADE, ALIVE_SHADE


def write_frames(grid_list: list[Grid], *, frames_dir: str | Path, dimension: Dimensions):
    """
    create frames based on a list of game states and write them to a given directory

    :param grid_list: list of grids containing each subsequent state from previously executed game of life
    :param frames_dir: temporary directory where frames will be located (this function is not responsible for cleanup)
    :param dimension: dimensions of the board
    :return: ``None``
    """

    def assume_scale_factor(dimension: Dimensions) -> int:
        max_dim = max(*dimension)
        return floor(MAX_RES / max_dim / 2) * 2

    for i, grid in enumerate(grid_list):
        # grid to frame
        image = np.full(dimension.astuple(), DEAD_SHADE, dtype=np.uint8)
        for x, y in grid:
            image[x][y] = ALIVE_SHADE

        # x_coords, y_coords = zip(*grid_list)
        # image[x_coords, y_coords] = WHITE

        # scale frame
        scale_factor = assume_scale_factor(dimension)
        image = np.kron(image, np.ones((scale_factor, scale_factor), dtype=image.dtype))

        # save frame
        file_path = os.path.join(frames_dir, f"{i:010}.{FRAME_EXT}")
        cv2.imwrite(file_path, image)


def render_frames(frames_dir: str | Path, framerate: int):
    output, _ = ffmpeg \
        .input(os.path.join(frames_dir, f"*.{FRAME_EXT}"), pattern_type="glob",
               framerate=framerate) \
        .output("testing.mp4").overwrite_output().run()


def assume_framerate(frames_count: int):
    framerate_stages = [
        # threshold, framerate
        (5, 2),
        (30, 5),
        (100, 10),
        (500, 15),
    ]
    fallback_framerate = 20

    for threshold, framerate in framerate_stages:
        if frames_count < threshold:
            return framerate
    return fallback_framerate
