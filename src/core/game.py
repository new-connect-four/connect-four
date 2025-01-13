from src.core import const


class Game:
    def __init__(self, rows=const.ROWS, columns=const.COLUMNS) -> None:
        self.rows = rows
        self.columns = columns
        self.board = self._create_board()
        self.winner = None
        self.current_player = const.PLAYER_ONE

    def new_game(self):
        self.current_player = const.PLAYER_ONE
        self.board = self._create_board()
        self.winner = None

    def make_move(self, column):
        if not self._is_valid_move(column):
            raise ValueError(const.INVALID_MOVE_ERROR)

        for row in reversed(range(self.rows)):
            if self.board[row][column] == 0:
                self.board[row][column] = self.current_player
                if self._check_winner(row, column):
                    self.winner = self.current_player
                self._change_current_player()
                return

        raise ValueError(const.FULL_COLUMN_ERROR)

    def _is_valid_move(self, column):
        return 0 <= column < self.columns and self.board[0][column] == 0

    def _change_current_player(self):
        self.current_player = (
            const.PLAYER_ONE if self.current_player == const.PLAYER_TWO else const.PLAYER_TWO
        )

    def _create_board(self):
        return [[0 for _ in range(self.columns)] for _ in range(self.rows)]

    def _check_winner(self, row, column):
        deltas = []

        deltas.append((0, 1))  # horizontal
        deltas.append((1, 0))  # vertical
        deltas.append((1, -1))  # diagonal \
        deltas.append((1, 1))  # diagonal /

        for delta in deltas:
            count = 1
            count += self._count(row, column, delta[0], delta[1])
            count += self._count(row, column, -delta[0], -delta[1])

            if count >= 4:
                return True

        return False

    def _count(self, row, column, delta_row, delta_column):
        count = 0
        current_player = self.current_player
        current_row, current_column = row + delta_row, column + delta_column

        while (
            0 <= current_row < self.rows
            and 0 <= current_column < self.columns
            and self.board[row][column] == current_player
        ):
            count += 1
            current_row += delta_row
            current_column += delta_column

        return count
