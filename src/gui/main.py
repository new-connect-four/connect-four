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

def button(text, width, height):
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    surface.fill((0, 0, 0, 0))

    text_font = pygame.font.SysFont('Arial', 32, bold=True)
    pygame.draw.rect(surface, theme.BOARD, pygame.Rect(0,0,width,height), border_radius=15)
    text_surface = text_font.render(text, True, (255,255,255))
    text_surface.convert_alpha()

    surface.blit(text_surface, ((width - text_surface.get_width())// 2, (height - text_surface.get_height()) // 2))
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

        self.reset_button = button("RESET", 250, 50)

        self.isRunning = True
        self.posX = 0

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
                draw_token(self.screen, (10 + j * (size * 2 + 10) + size), (500 - size - 10) - (size * 2 + 10) * (self.game.rows - i - 1), size, color)
                if j != self.game.columns - 1:
                    gfxdraw.line(self.screen, (10 + j * (size * 2 + 10) + size) + 35, (500 - size - 10) - (size * 2 + 10) * i - 30, (10 + j * (size * 2 + 10) + size) + 35, (500 - size - 10) - (size * 2 + 10) * i + 380, (0,100,155))

    def draw_drop(self, posX):
        pygame.draw.rect(self.screen, theme.BACKGROUND, (0,0, 500, 500))
        self.posX = posX
        draw_token(self.screen, min(max(self.posX, 40), 460), 35, 30,  self.player1_color if self.game.current_player == const.PLAYER_ONE else self.player2_color)

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
                if 0 < pos[0] < 500:
                    col = min((max(pos[0] - 5, 0)) // 70, 6)
                    try:
                        if self.game.winner:
                            continue
                        
                        self.game.make_move(col)
                        print('\n'.join([str(a) for a in self.game.board]))

                        draw_token(self.screen, min(max(self.posX, 40), 460), 35, 30,  self.player1_color if self.game.current_player == const.PLAYER_ONE else self.player2_color)
                        if self.game.winner is not None:
                            print("Wygrał", self.game.winner)
                    except Exception as e:
                        print(e)
                else:
                    if self.reset_button.get_rect().collidepoint((pos[0] - 500 - 25, pos[1] - 200)):
                        self.game.new_game()
                        self.screen.fill(theme.BACKGROUND)

    def run(self):
        while self.isRunning:
            self.handle_events()

            pygame.draw.rect(self.screen, theme.BOARD, pygame.Rect(0, 70, 500, 500), border_radius=10)
            self.draw_board()

            s = pygame.Surface((300,500))
            s.fill(theme.BACKGROUND)

            s.blit(self.player1_scoreboard, (25,45))
            s.blit(self.player2_scoreboard, (175,45))
            s.blit(self.reset_button, (25,200))

            self.screen.blit(s, (500, 0))

            pygame.display.flip()
            pygame.time.Clock().tick(60)
        pygame.quit()

if __name__ == "__main__":
    game = Connect4Game()
    game.run()
