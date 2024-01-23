import os
import unittest
import shutil
from tempfile import mkdtemp, TemporaryDirectory

from goltv.definitions import Grid, Dimensions
from goltv.renderer import write_frames, render_frames, assume_framerate


class TestRenderer(unittest.TestCase):
    def setUp(self):
        self.mock_grid_list = [Grid(), Grid(), Grid()]
        self.mock_dimensions = Dimensions(10, 10)

        self.mock_frames_dir = mkdtemp()
        self.mock_output_dir = mkdtemp()
        self.mock_output_file = os.path.join(self.mock_output_dir, "test_output_file.mp4")

    def tearDown(self):
        if os.path.exists(self.mock_output_file):
            os.remove(self.mock_output_file)
        shutil.rmtree(self.mock_output_dir)

        shutil.rmtree(self.mock_frames_dir)

    def test_write_frames(self):
        write_frames(self.mock_grid_list, frames_dir=self.mock_frames_dir, dimensions=self.mock_dimensions)
        self.assertEqual(len(os.listdir(self.mock_frames_dir)), len(self.mock_grid_list))

    def test_render_frames(self):
        write_frames(self.mock_grid_list, frames_dir=self.mock_frames_dir, dimensions=self.mock_dimensions)
        self.assertEqual(len(os.listdir(self.mock_frames_dir)), len(self.mock_grid_list))
        render_frames(self.mock_frames_dir, self.mock_output_file, framerate=20)
        self.assertTrue(os.path.exists(self.mock_output_file))


if __name__ == '__main__':
    unittest.main()
