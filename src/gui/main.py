from src.core.game import Game
from src.core import const
from pygame import gfxdraw
import pygame

import src.gui.theme as theme

def draw_token(surface, x, y, radius, color):
    gfxdraw.aacircle(surface, x, y, radius, color[1])
    gfxdraw.filled_circle(surface, x, y, radius,color[1])
    gfxdraw.aacircle(surface, x, y, radius - 4, color[0])
    gfxdraw.filled_circle(surface, x, y, radius - 4,color[0])

def scoreboard(text, color, score):
    surface = pygame.Surface((100,150))
    surface.convert_alpha()
    surface.fill(theme.BACKGROUND)

    text_font = pygame.font.SysFont('Arial', 16, bold=True)
    score_font = pygame.font.SysFont('Arial', 40, bold=True)

    pygame.draw.rect(surface, theme.BOARD, pygame.Rect(0,25,100,125), border_radius=10)
    draw_token(surface, 50, 25, 20, color)

    text_surface = text_font.render(text, True, (255, 255, 255))
    text_surface.convert_alpha()

    wins = score_font.render(str(score), True, (255,255,255))
    wins.convert_alpha()

    surface.blit(text_surface, ((100 - text_surface.get_width()) // 2,50))
    surface.blit(wins, ((100 - wins.get_width()) // 2,75))
    return surface

def button(text, width, height, highlight=False):
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    surface.fill((0, 0, 0, 0))

    text_font = pygame.font.SysFont('Arial', 32, bold=True)
    color = theme.BOARD_HIGHLIGHT if highlight else theme.BOARD
    pygame.draw.rect(surface, color, pygame.Rect(0, 0, width, height), border_radius=15)
    text_surface = text_font.render(text, True, (255,255,255))
    text_surface.convert_alpha()

    surface.blit(text_surface, ((width - text_surface.get_width()) // 2, (height - text_surface.get_height()) // 2))
    return surface

class Connect4Game:
    def __init__(self):
        self.game = Game()

        pygame.init()
        pygame.font.init()
        pygame.display.set_caption("Connect 4")
        
        self.screen = pygame.display.set_mode([800, 500])
        self.screen.convert_alpha()
        self.screen.fill(theme.BACKGROUND)

        self.player1_wins = 0
        self.player2_wins = 0

        self.player1_color = theme.YELLOW
        self.player2_color = theme.RED

        self.player1_scoreboard = scoreboard("PLAYER 1", self.player1_color, self.player1_wins)
        self.player2_scoreboard = scoreboard("AI", self.player2_color, self.player2_wins)

        self.new_game_button = button("X", 50, 50)

        self.isRunning = True
        self.posX = 0

    def update_scoreboards(self):
        self.player1_scoreboard = scoreboard("PLAYER 1", self.player1_color, self.player1_wins)
        self.player2_scoreboard = scoreboard("AI", self.player2_color, self.player2_wins)

    def draw_board(self):
        size = 30
        for i in range(self.game.rows):
            for j in range(self.game.columns):
                match (self.game.board[i][j]):
                    case 1:
                        color = self.player1_color
                    case 2:
                        color = self.player2_color
                    case _:
                        color = (theme.BACKGROUND, theme.BACKGROUND)

                draw_token(self.screen, (160 + j * (size * 2 + 10) + size), (500 - size - 10) - (size * 2 + 10) * (self.game.rows - i - 1), size, color)
                if j != self.game.columns - 1:
                    gfxdraw.line(self.screen, (160 + j * (size * 2 + 10) + size) + 35, (500 - size - 10) - (size * 2 + 10) * i - 30, (160 + j * (size * 2 + 10) + size) + 35, (500 - size - 10) - (size * 2 + 10) * i + 380, (0,100,155))

    def draw_drop(self, posX):
        pygame.draw.rect(self.screen, theme.BACKGROUND, (0,0, 800, 500))
        self.posX = posX
        draw_token(self.screen, min(max(self.posX, 190), 610), 35, 30, self.player1_color if self.game.current_player == const.PLAYER_ONE else self.player2_color)

    def winner_screen(self, winner_name, winner_color):
        overlay = pygame.Surface((800, 500), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        self.screen.blit(overlay, (0, 0))

        surface = pygame.Surface((400, 200), pygame.SRCALPHA)
        surface.fill((0, 0, 0, 0))

        winner_font = pygame.font.SysFont('Arial', 24, bold=True)

        pygame.draw.rect(surface, theme.BOARD, pygame.Rect(0, 0, 400, 200), border_radius=15)
        draw_token(surface, 200, 50, 30, winner_color)

        winner_text = winner_font.render(f"{winner_name} WINS!", True, (255, 255, 255))
        winner_text.convert_alpha()
        surface.blit(winner_text, ((400 - winner_text.get_width()) // 2, 100))

        new_game_button = button("NEW GAME", 200, 50)
        button_rect = new_game_button.get_rect(center=(200, 170))
        surface.blit(new_game_button, button_rect.topleft)

        self.screen.blit(surface, (200, 150))
        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEMOTION:
                    pos = pygame.mouse.get_pos()
                    highlight = button_rect.collidepoint(pos[0] - 200, pos[1] - 150)
                    new_game_button = button("NEW GAME", 200, 50, highlight)
                    surface.blit(new_game_button, button_rect.topleft)
                    self.screen.blit(surface, (200, 150))
                    pygame.display.flip()
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    if button_rect.collidepoint(pos[0] - 200, pos[1] - 150):
                        self.game.new_game()
                        self.screen.fill(theme.BACKGROUND)
                        return

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.isRunning = False
            if event.type == pygame.MOUSEMOTION:
                if self.game.winner is None:
                    self.draw_drop(event.pos[0])
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 4 or event.button == 5:  # Ignoruj scrolla myszy
                    continue
                pos = pygame.mouse.get_pos()
                if 150 < pos[0] < 650:
                    col = min((max(pos[0] - 155, 0)) // 70, 6)
                    try:
                        if self.game.winner:
                            continue
                        self.game.make_move(col)

                        print('\n'.join([str(a) for a in self.game.board]))
                        draw_token(self.screen, min(max(self.posX, 190), 610), 35, 30, self.player1_color if self.game.current_player == const.PLAYER_ONE else self.player2_color)

                        if self.game.winner is not None:
                            print("Wygrał", self.game.winner)
                            winner_name = "PLAYER 1" if self.game.winner == const.PLAYER_ONE else "AI"
                            winner_color = self.player1_color if self.game.winner == const.PLAYER_ONE else self.player2_color
                            if self.game.winner == const.PLAYER_ONE:
                                self.player1_wins += 1
                            else:
                                self.player2_wins += 1
                            self.update_scoreboards()
                            self.draw_board()
                            pygame.display.flip()
                            pygame.time.delay(200)
                            self.winner_screen(winner_name, winner_color)
                    except Exception as e:
                        print(e)
                else:
                    if self.new_game_button.get_rect().collidepoint((pos[0] - 25, pos[1] - 25)):
                        self.game.new_game()
                        self.screen.fill(theme.BACKGROUND)
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if self.player1_scoreboard.get_rect(topleft=(25, 155)).collidepoint(pos):
                    self.player1_color = self.get_next_color(self.player1_color, self.player2_color)
                    self.update_scoreboards()
                if self.player2_scoreboard.get_rect(topleft=(675, 155)).collidepoint(pos):
                    self.player2_color = self.get_next_color(self.player2_color, self.player1_color)
                    self.update_scoreboards()

    def get_next_color(self, current_color, other_color):
        colors = [theme.YELLOW, theme.RED, theme.GREEN, theme.PURPLE, theme.WHITE, theme.BLACK]
        next_index = (colors.index(current_color) + 1) % len(colors)
        next_color = colors[next_index]
        if next_color == other_color:
            next_index = (next_index + 1) % len(colors)
            next_color = colors[next_index]
        return next_color

    def run(self):
        while self.isRunning:
            self.handle_events()

            pygame.draw.rect(self.screen, theme.BOARD, pygame.Rect(150, 70, 500, 500), border_radius=10)
            self.draw_board()

            self.screen.blit(self.player1_scoreboard, (25, 155))
            self.screen.blit(self.player2_scoreboard, (675, 155))
            self.screen.blit(self.new_game_button, (5, 5))

            pygame.display.flip()
            pygame.time.Clock().tick(60)
        pygame.quit()

if __name__ == "__main__":
    game = Connect4Game()
    game.run()
