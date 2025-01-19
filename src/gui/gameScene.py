import sys
import pygame
from pygame import gfxdraw

from src.core.game import Game
from src.core.bot import Bot

from src.core import const
from src.gui import theme
from src.gui.draw import draw_token, button, scoreboard


def clamp(minimum, val, maximum):
    return max(minimum, min(val, maximum))


class Player:
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.wins = 0

    def add_win(self):
        self.wins += 1


class GameScene:
    def __init__(self, screen, scene_manager):
        self.screen = screen
        self.scene_manager = scene_manager

        self.font = pygame.font.SysFont("Arial", 36)

        self.title_text = self.font.render("New Game", True, (255, 255, 255))
        self.title_rect = self.title_text.get_rect(
            center=(screen.get_width() // 2, 100)
        )

        self.back_button = button("X", 40, 40, fontSize=20)
        self.reset_button = button("Reset", 80, 40, fontSize=20)

        self.player1 = Player("PLAYER 1", theme.YELLOW)
        self.player2 = Player("PLAYER 2", theme.RED)

        self.posX = 0

    def setup(self, **options):
        self.game = Game()
        self.bot = Bot(self.game)

        self.playWithBot = options.get("playWithBot", False)

        self.player1_scoreboard = scoreboard(
            self.player1.name, self.player1.color, self.player1.wins
        )
        self.player2_scoreboard = scoreboard(
            self.player2.name, self.player2.color, self.player2.wins
        )

        self.player2.name = "BOT" if self.playWithBot else "PLAYER 2"

        self.draw_drop(pygame.mouse.get_pos()[0])

    def cleanup(self):
        pass

    def update(self):
        pass

    def render(self):
        pygame.draw.rect(
            self.screen, theme.BOARD, pygame.Rect(150, 70, 500, 500), border_radius=10
        )
        self.draw_board()

        self.screen.blit(self.player1_scoreboard, (25, 155))
        self.screen.blit(self.player2_scoreboard, (675, 155))
        self.screen.blit(self.back_button, (5, 5))
        self.screen.blit(self.reset_button, (50, 5))

    def update_scoreboards(self):
        self.player1_scoreboard = scoreboard(
            self.player1.name, self.player1.color, self.player1.wins
        )
        self.player2_scoreboard = scoreboard(
            self.player2.name, self.player2.color, self.player2.wins
        )

    def draw_drop(self, posX):
        pygame.draw.rect(self.screen, theme.BACKGROUND, (0, 0, 800, 500))
        self.posX = posX
        draw_token(
            self.screen,
            clamp(190, self.posX, 610),
            35,
            30,
            self.player1.color
            if self.game.current_player == const.PLAYER_ONE
            else self.player2.color,
        )

    def game_over_screen(self, winner_name, winner_color, draw=False):
        overlay = pygame.Surface((800, 500), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        self.screen.blit(overlay, (0, 0))

        surface = pygame.Surface((400, 200), pygame.SRCALPHA)
        surface.fill((0, 0, 0, 0))

        winner_font = pygame.font.SysFont("Arial", 24, bold=True)

        pygame.draw.rect(
            surface, theme.BOARD, pygame.Rect(0, 0, 400, 200), border_radius=15
        )

        if not draw:
            draw_token(surface, 200, 50, 30, winner_color)

        winner_text = winner_font.render(
            f"{winner_name} WINS!" if not draw else "DRAW!", True, (255, 255, 255)
        )
        winner_text.convert_alpha()

        surface.blit(winner_text, ((400 - winner_text.get_width()) // 2, 100))

        new_game_button = button("NEW GAME", 200, 50)
        button_rect = new_game_button.get_rect(center=(200, 170))

        surface.blit(new_game_button, button_rect.topleft)

        self.screen.blit(surface, (200, 150))
        pygame.display.flip()

        self.update_scoreboards()

        while True:
            for event in pygame.event.get():
                match event.type:
                    case pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    case pygame.MOUSEMOTION:
                        pos = pygame.mouse.get_pos()
                        highlight = button_rect.collidepoint(pos[0] - 200, pos[1] - 150)
                        new_game_button = button("NEW GAME", 200, 50, highlight)
                        surface.blit(new_game_button, button_rect.topleft)
                        self.screen.blit(surface, (200, 150))
                        pygame.display.flip()
                    case pygame.MOUSEBUTTONUP:
                        pos = pygame.mouse.get_pos()
                        if button_rect.collidepoint(pos[0] - 200, pos[1] - 150):
                            self.game.new_game()
                            self.screen.fill(theme.BACKGROUND)
                            self.render()
                            return

    def handle_event(self, event):
        match event.type:
            case pygame.MOUSEMOTION:
                if self.game.winner is None:
                    self.draw_drop(event.pos[0])

            case pygame.MOUSEBUTTONUP:
                if event.button in (4, 5):
                    return
                pos = pygame.mouse.get_pos()
                if 150 < pos[0] < 650:
                    col = clamp(0, (pos[0] - 155) // 70, 6)
                    try:
                        if self.game.winner:
                            return
                        self.game.make_move(col)

                        print("\n".join([str(a) for a in self.game.board]))
                        color = (
                            self.player1.color
                            if self.game.current_player == const.PLAYER_ONE
                            else self.player2.color
                        )
                        if self.playWithBot:
                            color = self.player1.color
                        draw_token(
                            self.screen, clamp(190, self.posX, 610), 35, 30, color
                        )

                        if self.playWithBot:
                            try:
                                self.bot.make_move()
                            except Exception as e:
                                print(e)

                        if 0 not in sum(self.game.board, []):
                            self.draw_board()
                            pygame.display.flip()
                            pygame.time.delay(200)
                            self.render()
                            self.game_over_screen(None, None, draw=True)

                        if self.game.winner is not None:
                            print("Wygrał", self.game.winner)
                            winner = (
                                self.player1
                                if self.game.winner == const.PLAYER_ONE
                                else self.player2
                            )
                            winner.add_win()
                            self.update_scoreboards()
                            self.draw_board()
                            pygame.display.flip()
                            pygame.time.delay(200)
                            self.render()
                            self.game_over_screen(winner.name, winner.color)
                    except Exception as e:
                        print(e)
                else:
                    if self.back_button.get_rect().collidepoint(
                        (pos[0] - 5, pos[1] - 5)
                    ):
                        self.screen.fill(theme.BACKGROUND)
                        self.scene_manager.switch_scene("MainMenuScene")

                    if self.reset_button.get_rect().collidepoint(
                        (pos[0] - 50, pos[1] - 5)
                    ):
                        self.game.new_game()
                        self.player1.wins = 0
                        self.player2.wins = 0
                        self.update_scoreboards()
                        self.screen.fill(theme.BACKGROUND)

            case pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if self.player1_scoreboard.get_rect(topleft=(25, 155)).collidepoint(
                    pos
                ):
                    self.player1.color = self.get_next_color(
                        self.player1.color, self.player2.color
                    )
                    self.update_scoreboards()
                if self.player2_scoreboard.get_rect(topleft=(675, 155)).collidepoint(
                    pos
                ):
                    self.player2.color = self.get_next_color(
                        self.player2.color, self.player1.color
                    )
                    self.update_scoreboards()

            case pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.scene_manager.switch_scene("MainMenuScene")

    def handle_selection(self):
        print("Starting a new game")

    def draw_board(self):
        size = 30
        for i in range(self.game.rows):
            for j in range(self.game.columns):
                match self.game.board[i][j]:
                    case 1:
                        color = self.player1.color
                    case 2:
                        color = self.player2.color
                    case _:
                        color = (theme.BACKGROUND, theme.BACKGROUND)

                draw_token(
                    self.screen,
                    (160 + j * (size * 2 + 10) + size),
                    (500 - size - 10) - (size * 2 + 10) * (self.game.rows - i - 1),
                    size,
                    color,
                )
                if j != const.COLUMNS - 1:
                    gfxdraw.line(
                        self.screen,
                        (160 + j * (size * 2 + 10) + size) + 35,
                        (500 - size - 10) - (size * 2 + 10) * i - 30,
                        (160 + j * (size * 2 + 10) + size) + 35,
                        (500 - size - 10) - (size * 2 + 10) * i + 380,
                        (0, 100, 155),
                    )

    def get_next_color(self, current_color, other_color):
        colors = [
            theme.YELLOW,
            theme.RED,
            theme.GREEN,
            theme.PURPLE,
            theme.WHITE,
            theme.BLACK,
        ]
        next_index = (colors.index(current_color) + 1) % len(colors)
        next_color = colors[next_index]
        if next_color == other_color:
            next_index = (next_index + 1) % len(colors)
            next_color = colors[next_index]
        return next_color
