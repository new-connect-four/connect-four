import random
from src.core.game import Game
from src.core import const

class Bot:
    def __init__(self, game: Game):
        self.game = game

    def make_move(self):
        if self.game.winner is not None:
            raise ValueError("The game is already over.")

        for col in range(self.game.columns):
            if self.game._is_valid_move(col):
                if self._can_win_next_move(col):
                    self.game.make_move(col)
                    return

        for col in range(self.game.columns):
            if self.game._is_valid_move(col):
                if self._can_opponent_win_next_move(col):
                    self.game.make_move(col)
                    return

        valid_columns = [col for col in range(self.game.columns) if self.game._is_valid_move(col)]
        if not valid_columns:
            raise ValueError("No valid moves available.")

        chosen_column = random.choice(valid_columns)
        self.game.make_move(chosen_column)

    def _can_win_next_move(self, column):
        temp_game = self._simulate_move(column, const.PLAYER_TWO)
        return temp_game.winner == const.PLAYER_TWO

    def _can_opponent_win_next_move(self, column):
        temp_game = self._simulate_move(column, const.PLAYER_ONE)
        return temp_game.winner == const.PLAYER_ONE

    def _simulate_move(self, column, player):
        simulated_game = Game(self.game.rows, self.game.columns)
        simulated_game.board = [row[:] for row in self.game.board]
        simulated_game.current_player = player
        simulated_game.make_move(column)
        return simulated_game
