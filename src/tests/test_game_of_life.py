import unittest

from goltv.converters import grid_from_string
from goltv.definitions import Dimensions, Cell, Grid
from goltv.game_of_life import execute_full_game, within_dimensions, get_neighbors, \
    next_round


class TestGameOfLife(unittest.TestCase):

    def test_within_dimensions(self):
        dimensions = Dimensions(5, 5)
        self.assertTrue(within_dimensions(dimensions, Cell(2, 2)))
        self.assertFalse(within_dimensions(dimensions, Cell(5, 5)))
        self.assertTrue(within_dimensions(dimensions, Cell(0, 0)))
        self.assertFalse(within_dimensions(dimensions, Cell(-1, 0)))

    def test_get_neighbors(self):
        grid = grid_from_string("0 0  0 1  0 2")
        alive_neighbors, dead_neighbors = get_neighbors(grid, 0, 1)
        self.assertEqual(alive_neighbors, {Cell(0, 0),
                                           Cell(0, 2)})
        self.assertEqual(dead_neighbors, {Cell(x=1, y=2),
                                          Cell(x=-1, y=1),
                                          Cell(x=1, y=1),
                                          Cell(x=-1, y=0),
                                          Cell(x=1, y=0),
                                          Cell(x=-1, y=2)})

    def test_execute_full_game(self):
        initial_grid = grid_from_string("0 0  0 1  0 2")
        dimensions = Dimensions(3, 3)
        result = execute_full_game(initial_grid, dimensions=dimensions)
        expected_result = [
            {Cell(0, 0), Cell(0, 1), Cell(0, 2)},
            {Cell(0, 1), Cell(1, 1)},
            Grid()
        ]
        self.assertEqual(result, expected_result)

    def test_next_round_with_stable_structure(self):
        test_cases = [
            # grid, expected next round
            ("1 1  1 2  2 1  2 2", "1 1  1 2  2 1  2 2"),
            ("1 0  1 1  1 2", "0 1  1 1  2 1"),
            ("1 1", ""),
            ("1 1  1 2  2 1  2 2  3 1", "1 2  3 1  1 1  2 0  3 2"),
            ("0 1  1 1  2 1", "1 0  1 1  1 2"),
        ]

        for grid, expected_next_round in test_cases:
            grid = grid_from_string(grid)
            expected_next_round = grid_from_string(expected_next_round)

            self.assertEqual(next_round(grid), expected_next_round)
