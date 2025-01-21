import unittest

from src.core import const
from src.core.game import Game


class TestGame(unittest.TestCase):
    def setUp(self):
        self.game = Game()
        return super().setUp()

    def test_initial_state(self):
        self.assertEqual(self.game.rows, const.ROWS)
        self.assertEqual(self.game.columns, const.COLUMNS)
        self.assertEqual(self.game.current_player, const.PLAYER_ONE)
        self.assertIsNone(self.game.winner)
        self.assertEqual(len(self.game.board), const.ROWS)
        self.assertEqual(len(self.game.board[0]), const.COLUMNS)
        self.assertTrue(
            all(cell == 0 for row in self.game.board for cell in row)
        )

    def test_new_game(self):
        self.game.current_player = const.PLAYER_TWO
        self.game.board[0][0] = const.PLAYER_ONE

        self.game.new_game()
        self.assertEqual(self.game.current_player, const.PLAYER_ONE)
        self.assertTrue(
            all(cell == 0 for row in self.game.board for cell in row)
        )
        self.assertIsNone(self.game.winner)

    def test_valid_move(self):
        self.game.make_move(0)
        self.assertEqual(self.game.board[-1][0], const.PLAYER_ONE)
        self.assertEqual(self.game.current_player, const.PLAYER_TWO)

    def test_invalid_move(self):
        with self.assertRaises(ValueError) as context:
            self.game.make_move(-1)
        self.assertEqual(str(context.exception), const.INVALID_MOVE_ERROR)

    def test_change_player(self):
        self.assertEqual(self.game.current_player, const.PLAYER_ONE)
        self.game.make_move(0)
        self.assertEqual(self.game.current_player, const.PLAYER_TWO)
        self.game.make_move(1)
        self.assertEqual(self.game.current_player, const.PLAYER_ONE)

    def test_no_winner(self):
        self.game.make_move(0)
        self.assertIsNone(self.game.winner)


if __name__ == "__main__":
    unittest.main()
