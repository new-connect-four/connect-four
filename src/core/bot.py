import random
from src.core.game import Game
from src.core import const

class Bot:
    def __init__(self, game: Game, algorithm: str = "rand"):
        if algorithm not in {"rand", "minimax"}:
            raise ValueError("Incorrect bot algorithm.")
        self.game = game
        self.algorithm = algorithm
        self.weights = None

        if algorithm == "minimax":
            self.weights = self._calculate_weights()

    def make_move(self):
        if self.game.winner is not None:
            raise ValueError("The game is already over.")

        valid_columns = [col for col in range(self.game.columns) if self.game._is_valid_move(col)]
        if not valid_columns:
            raise ValueError("No valid moves available.")

        chosen_column = None
        if self.algorithm == "rand":
            chosen_column = self._find_move_rand()
        elif self.algorithm == "minimax":
            chosen_column = self._find_move_minimax(5)

        self.game.make_move(chosen_column)

    def _can_win_next_move(self, column, game_state: Game = None):
        temp_game = self._simulate_move(column, const.PLAYER_TWO, game_state)
        return temp_game.winner == const.PLAYER_TWO

    def _can_opponent_win_next_move(self, column, game_state: Game = None):
        temp_game = self._simulate_move(column, const.PLAYER_ONE, game_state)
        return temp_game.winner == const.PLAYER_ONE

    def _simulate_move(self, column, player, game_state: Game = None):
        if game_state is None:
            game_state = self.game
        simulated_game = Game(game_state.rows, game_state.columns)
        simulated_game.board = [row[:] for row in game_state.board]
        simulated_game.current_player = player
        simulated_game.make_move(column)
        return simulated_game

    def _calculate_weights(self):
        weights = [[0] * self.game.columns for _ in range(self.game.rows)]

        for col in range(self.game.columns):
            for row in range(self.game.rows - 3):
                weights[row][col] += 1
                weights[row + 1][col] += 1
                weights[row + 2][col] += 1
                weights[row + 3][col] += 1

        for row in range(self.game.rows):
            for col in range(self.game.columns - 3):
                weights[row][col] += 1
                weights[row][col + 1] += 1
                weights[row][col + 2] += 1
                weights[row][col + 3] += 1

        for row in range(self.game.rows - 3):
            for col in range(self.game.columns - 3):
                weights[row][col] += 1
                weights[row + 1][col + 1] += 1
                weights[row + 2][col + 2] += 1
                weights[row + 3][col + 3] += 1

        for row in range(self.game.rows - 3):
            for col in range(3, self.game.columns):
                weights[row][col] += 1
                weights[row + 1][col - 1] += 1
                weights[row + 2][col - 2] += 1
                weights[row + 3][col - 3] += 1

        return weights

    def _eval_board(self, game_state: Game):
        total_score = 0
        ai_score = 0
        player_score = 0

        for row in range(game_state.rows):
            for col in range(game_state.columns):
                if game_state.board[row][col] == const.PLAYER_TWO:
                    ai_score += self.weights[row][col]
                elif game_state.board[row][col] == const.PLAYER_ONE:
                    player_score += self.weights[row][col]

        total_score = ai_score - player_score
        return total_score

    def _minimax(self, moves, depth, alpha, beta, player):
        valid_columns = [col for col in range(self.game.columns) if moves._is_valid_move(col)]

        for col in valid_columns:
            if self._can_win_next_move(col, moves):
                return col, float('inf')

        for col in valid_columns:
            if self._can_opponent_win_next_move(col, moves):
                return col, float('-inf') 

        #remis
        if(all(moves.board[0][col] != 0 for col in range(self.game.columns))):
            return None, 0

        if depth == 0:
            return None, self._eval_board(moves)

        #ai
        if player == const.PLAYER_TWO:
            score = float('-inf')
            column = valid_columns[0]
            for col in valid_columns:
                new_move = self._simulate_move(col, const.PLAYER_TWO)
                _, new_score = self._minimax(new_move, depth-1, alpha, beta, const.PLAYER_ONE)

                if new_score > score:
                    score = new_score
                    column = col

                alpha = max(alpha, score)
                if alpha >= beta:
                    break
            
            return column, score
        #czlowiek
        else:
            score = float('inf')
            column = valid_columns[0]
            for col in valid_columns:
                new_move = self._simulate_move(col, const.PLAYER_ONE)
                _, new_score = self._minimax(new_move, depth-1, alpha, beta, const.PLAYER_TWO)

                if new_score < score:
                    score = new_score
                    column = col

                beta = min(beta, score)
                if alpha >= beta:
                    break

            return column, score

    def _find_move_minimax(self, depth):
        col, _ = self._minimax(self.game, depth, float('-inf'), float('inf'), const.PLAYER_TWO)
        return col

    def _find_move_rand(self):
        valid_columns = [col for col in range(self.game.columns) if self.game._is_valid_move(col)]

        for col in range(self.game.columns):
            if self.game._is_valid_move(col):
                if self._can_win_next_move(col):
                    return col

        for col in range(self.game.columns):
            if self.game._is_valid_move(col):
                if self._can_opponent_win_next_move(col):
                    return col

        chosen_column = random.choice(valid_columns)
        return chosen_column