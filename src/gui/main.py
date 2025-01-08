from src.core.game import Game
from src.core.const import ROWS, COLUMNS
from pygame import gfxdraw
import pygame

import src.gui.theme as theme

# REMOVE
board = [[0 for _ in range(COLUMNS)] for _ in range(ROWS)]

board[1][1] = 1

board[2][6] = 2
# REMOVE

def draw_token(surface, x, y, radius, color):
    gfxdraw.aacircle(surface, x, y, radius, color[1])
    gfxdraw.filled_circle(surface, x, y, radius,color[1])
    gfxdraw.aacircle(surface, x, y, radius - 4, color[0])
    gfxdraw.filled_circle(surface, x, y, radius - 4,color[0])

def main():
    game = Game()
    pygame.init()
    screen = pygame.display.set_mode([800, 500])
    screen.convert_alpha()
    pygame.display.set_caption("Connect 4")
    screen.fill(theme.BACKGROUND)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.draw.rect(screen, theme.BOARD, pygame.Rect(0, 70, 500, 500))

        size = 30
        for j in range(COLUMNS):
            for i in range(ROWS):
                color = (theme.BACKGROUND, theme.BACKGROUND)
                if board[i][j] == 1:
                    color = theme.YELLOW
                elif board[i][j] == 2:
                    color = theme.RED
                draw_token(screen, (10 + j * (size * 2 + 10) + size), (500 - size - 10) - (size * 2 + 10) * i, size, color)

        pygame.display.flip()
        pygame.time.Clock().tick(60)
    pygame.quit()

if __name__ == "__main__":
    main()
