from src.core import const


class Game:
    def __init__(self, rows = const.ROWS, colums = const.COLUMNS) -> None:
        self.rows = rows
        self.columns = colums
        self.board = self._create_board()
        self.winner = None
        self.current_player = const.PLAYER_ONE

    def _create_board(self):
        return [[0 for _ in range(self.columns)] for _ in range(self.rows)]

    def add_piece(self):
        raise NotImplementedError()

    def _is_valid_move(self):
        raise NotImplementedError()

    def _check_winner(self):
        raise NotImplementedError()

    def new_game(self):
        self.current_player = const.PLAYER_ONE
        self.board = self._create_board()
        self.winner = None
