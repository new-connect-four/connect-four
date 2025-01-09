from src.core.game import Game
from src.core.const import ROWS, COLUMNS
from pygame import gfxdraw
import pygame

import src.gui.theme as theme

def draw_token(surface, x, y, radius, color):
    gfxdraw.aacircle(surface, x, y, radius, color[1])
    gfxdraw.filled_circle(surface, x, y, radius,color[1])
    gfxdraw.aacircle(surface, x, y, radius - 4, color[0])
    gfxdraw.filled_circle(surface, x, y, radius - 4,color[0])

class Connect4Game:
    def __init__(self):
        self.game = Game()
        
        pygame.init()
        pygame.display.set_caption("Connect 4")
        
        self.screen = pygame.display.set_mode([800, 500])
        self.screen.convert_alpha()
        self.screen.fill(theme.BACKGROUND)

        self.isRunning = True
        self.posX = 0

        # REMOVE
        self.board = [[0 for _ in range(COLUMNS)] for _ in range(ROWS)]
        self.player1 = True
        # REMOVE

    def draw_board(self):
        size = 30
        for j in range(COLUMNS):
            for i in range(ROWS):
                match (self.board[i][j]):
                    case 1:
                        color = theme.YELLOW
                    case 2:
                        color = theme.RED
                    case _:
                        color = (theme.BACKGROUND, theme.BACKGROUND)
                draw_token(self.screen, (10 + j * (size * 2 + 10) + size), (500 - size - 10) - (size * 2 + 10) * i, size, color)
    
    def draw_drop(self, posX):
        pygame.draw.rect(self.screen, theme.BACKGROUND, (0,0, 500, 500))
        self.posX = posX
        draw_token(self.screen, min(max(self.posX, 40), 460), 35, 30, theme.YELLOW if self.player1 else theme.RED)
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.isRunning = False
            if event.type == pygame.MOUSEMOTION:
               self.draw_drop(event.pos[0])
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                if 0 < pos[0] < 500:
                    col = min((max(pos[0] - 5, 0)) // 70, 6)
                    s = False
                    for _ in range(ROWS):
                        if self.board[_][col] == 0:
                            self.board[_][col] = 1 if self.player1 else 2
                            s = True
                            break
                    if not s:
                        continue
                    self.player1 = not self.player1
                    draw_token(self.screen, min(max(self.posX, 40), 460), 35, 30, theme.YELLOW if self.player1 else theme.RED)
    
    def run(self):
        while self.isRunning:
            self.handle_events()
            pygame.draw.rect(self.screen, theme.BOARD, pygame.Rect(0, 70, 500, 500), border_radius=10)
            self.draw_board()
            pygame.display.flip()
            pygame.time.Clock().tick(60)
        pygame.quit()

if __name__ == "__main__":
    game = Connect4Game()
    game.run()
