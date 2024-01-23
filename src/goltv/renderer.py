from pathlib import Path
from math import floor
import os
from typing import Optional

import cv2
import numpy as np
import ffmpeg

from goltv.definitions import Grid, Dimensions
from goltv.constants import FRAME_EXT, MAX_RES, DEAD_SHADE, ALIVE_SHADE, AUTO_FRAMERATE_THRESHOLDS, \
    AUTO_FRAMERATE_FALLBACK


def write_frames(grid_list: list[Grid], *, frames_dir: str | Path, dimensions: Dimensions,
                 scale_factor: Optional[int] = None):
    """
    Create frames based on a list of game states and write them to a given directory.

    :param grid_list: List of grids containing each subsequent state from previously executed game of life
    :param frames_dir: Temporary directory where frames will be located (this function is not responsible for cleanup)
    :param dimensions: Dimensions of the board
    :param scale_factor: A factor by which the grid will be scaled before creating frames
    :return: None
    """
    print("creating frames...")

    for i, grid in enumerate(grid_list):
        # grid to frame
        image = np.full(dimensions.astuple(), DEAD_SHADE, dtype=np.uint8)
        for x, y in grid:
            image[x][y] = ALIVE_SHADE

        # scale frame
        if scale_factor is None:
            # bigger dimension scaled up to the MAX_RES while being divisible by 2
            scale_factor = floor(MAX_RES / max(*dimensions) / 2) * 2
        image = np.kron(image, np.ones((scale_factor, scale_factor), dtype=image.dtype))

        # save frame
        file_path = os.path.join(frames_dir, f"{i:010}.{FRAME_EXT}")
        cv2.imwrite(file_path, image)


def render_frames(frames_dir: str | Path, output_file: str | Path, framerate: int):
    """
    Renders frames placed inside ``frames_dir`` to an ``output_file`` using ffmpeg.
    It takes all the frames that have ``FRAME_EXT`` extension.

    :param frames_dir: Location of the frames
    :param output_file: Output file path for the rendered video
    :param framerate: Framerate for the rendered video
    :return: None
    """
    print("saving video...")
    output, _ = ffmpeg \
        .input(os.path.join(frames_dir, f"*.{FRAME_EXT}"), pattern_type="glob",
               framerate=framerate) \
        .output(output_file) \
        .run()


def assume_framerate(frames_count: int):
    for threshold, framerate in AUTO_FRAMERATE_THRESHOLDS:
        if frames_count < threshold:
            return framerate
    return AUTO_FRAMERATE_FALLBACK
