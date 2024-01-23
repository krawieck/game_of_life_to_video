import unittest

from goltv.converters import grid_from_string, board_from_string
from goltv.definitions import Dimensions, Cell


class TestGameOfLife(unittest.TestCase):
    def test_grid_from_string(self):
        result = grid_from_string("0 0  0 1  0 2")
        expected_result = {Cell(0, 0),
                           Cell(0, 1),
                           Cell(0, 2)}
        self.assertEqual(result, expected_result)

        with self.assertRaises(ValueError):
            grid_from_string("sadfads")

    def test_board_from_string(self):
        text = "10\n01"
        board = board_from_string(text)
        self.assertEqual(board.dim, Dimensions(2, 2))
        self.assertEqual(len(board.grid), 2)


if __name__ == '__main__':
    unittest.main()
