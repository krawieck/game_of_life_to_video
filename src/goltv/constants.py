"""
This file contains all the necessary constantants.
"""
from math import inf

FRAME_LIMIT = 999999
"""Max number of frames """

MAX_RES = 2160
"""Resolution that will be strived for for the video if the scale factor was not specified"""

ALIVE_SHADE = 255
"""Lightness value of the alive cells"""

DEAD_SHADE = 0
"""Lightness value of the dead cells"""

FRAME_EXT = "png"
"""Extension used for the inter"""

OUTPUT_EXTS = ".mp4", ".mov", ".avi", ".webm", ".wmv", ".mkv", ".m4v"
"""Acceptable output video extensions"""

AUTO_FRAMERATE_THRESHOLDS = [
    # threshold, framerate
    (5, 2),
    (30, 5),
    (100, 10),
    (500, 15),
]
"""Thresholds and respective framerates that will be applied to a video that hadn't had the framerate specified"""

AUTO_FRAMERATE_FALLBACK = 20
"""Fallback framerate if the number of frames exceeds all the thresholds"""
