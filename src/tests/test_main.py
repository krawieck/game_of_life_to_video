import unittest
from unittest.mock import patch

from click import BadParameter

from goltv.main import play_game_and_render_it, DimensionsClickType, board_from_string
from goltv.definitions import Board, Dimensions, Grid


class TestMain(unittest.TestCase):

    @patch('goltv.main.execute_full_game')
    @patch('goltv.main.write_frames')
    @patch('goltv.main.assume_framerate')
    @patch('goltv.main.render_frames')
    def test_play_game_and_render_it(self, mock_render_frames, mock_assume_framerate, mock_write_frames,
                                     mock_execute_full_game):
        board = Board(Dimensions(10, 10), Grid())
        mock_execute_full_game.return_value = [Grid()]
        play_game_and_render_it(board)
        mock_execute_full_game.assert_called_once_with(board.grid, dimensions=board.dim)
        mock_write_frames.assert_called()
        mock_assume_framerate.assert_called()
        mock_render_frames.assert_called()

    def test_DimensionsClickType(self):
        dimensions_type = DimensionsClickType()
        self.assertEqual(dimensions_type.convert("120x140", None, None), Dimensions(120, 140))
        self.assertEqual(dimensions_type.convert(None, None, None), None)

        with self.assertRaises(BadParameter):
            dimensions_type.convert("120x140x160", None, None)
        with self.assertRaises(BadParameter):
            dimensions_type.convert("sjdfbajs", None, None)


if __name__ == '__main__':
    unittest.main()
