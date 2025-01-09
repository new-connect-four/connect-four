from src.core.game import Game
from src.core.const import ROWS, COLUMNS
from pygame import gfxdraw
import pygame

import src.gui.theme as theme

# REMOVE | DEBUG
board = [[0 for _ in range(COLUMNS)] for _ in range(ROWS)]

# REMOVE

def draw_token(surface, x, y, radius, color):
    gfxdraw.aacircle(surface, x, y, radius, color[1])
    gfxdraw.filled_circle(surface, x, y, radius,color[1])
    gfxdraw.aacircle(surface, x, y, radius - 4, color[0])
    gfxdraw.filled_circle(surface, x, y, radius - 4,color[0])

def draw_board(screen):
    size = 30
    for j in range(COLUMNS):
        for i in range(ROWS):
            color = (theme.BACKGROUND, theme.BACKGROUND)
            if board[i][j] == 1:
                color = theme.YELLOW
            elif board[i][j] == 2:
                color = theme.RED
            draw_token(screen, (10 + j * (size * 2 + 10) + size), (500 - size - 10) - (size * 2 + 10) * i, size, color)

def main():

    # REMOVE
    global player1
    player1 = True
    # REMOVE

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
            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, theme.BACKGROUND, (0,0, 500, 500))
                posx = event.pos[0]
                draw_token(screen, min(max(posx, 40), 460), 35, 30, theme.YELLOW if player1 else theme.RED)
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                if 0 < pos[0] < 500:
                    col = min((max(pos[0] - 5, 0)) // 70, 6)
                    s = False
                    for _ in range(ROWS):
                        if board[_][col] == 0:
                            board[_][col] = 1 if player1 else 2
                            s = True
                            break
                    if not s:
                        continue
                    player1 = not player1
                    draw_token(screen, min(max(posx, 40), 460), 35, 30, theme.YELLOW if player1 else theme.RED)
        pygame.draw.rect(screen, theme.BOARD, pygame.Rect(0, 70, 500, 500))

        draw_board(screen)

        pygame.display.flip()
        pygame.time.Clock().tick(60)
    pygame.quit()

if __name__ == "__main__":
    main()
