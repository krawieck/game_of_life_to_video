from pathlib import Path
from hashlib import md5
from time import time
import os

import cv2
import numpy as np
import ffmpeg

from definitions import Grid, Cell, Dimension
from constants import WHITE, FRAME_EXT


def _scale_up(pixel_grid_list, dimension: Dimension):
    def scale_factor():
        pass


def calc_padding(dimension: Dimension):
    return 1


def render_video(grid_list: list[Grid], tmp_dir: str | Path, dimension: Dimension):
    job_id: str = md5(str(time()).encode()).hexdigest()  # time to md5 hash
    padding = calc_padding(dimension)

    # MAKE FRAMES

    # make dir
    frames_dir = os.path.join(tmp_dir, job_id)
    frames_dir = os.path.join(os.curdir, job_id)  # TEMPORARY
    os.makedirs(frames_dir)

    for i, grid in enumerate(grid_list):
        # grid to frame
        print(f'make frame {i}')
        image = np.zeros(dimension.astuple(), dtype=np.uint8)
        # for x, y in grid:
        #     image[x][y] = WHITE
        x_coords, y_coords = zip(*grid_list)
        image[x_coords, y_coords] = WHITE

        # add padding
        # image = np.pad(image, pad_width=padding, mode="constant", constant_values=0)

        # scale frame
        # image =

        # save frame
        file_path = os.path.join(frames_dir, f"{i}.{FRAME_EXT}")
        cv2.imwrite(file_path, image)

    # FRAMES TO VIDEO

    # TODO: framerate based on number of frames

    def get_framerate():
        frames_count = len(grid_list)
        if frames_count < 5:
            return 2
        if frames_count < 30:
            return 5
        if frames_count < 100:
            return 10
        if frames_count < 500:
            return 15
        return 20

    print("ffmpeg time")
    output, _ = ffmpeg.input(os.path.join(frames_dir, f"*.{FRAME_EXT}"), pattern_type="glob",
                             framerate=get_framerate()).output("testing.mp4").overwrite_output().run(
        capture_stdout=True)
    print(output)
