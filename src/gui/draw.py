import pygame
from pygame import gfxdraw

from src.gui import theme


def scoreboard(text, color, score):
    surface = pygame.Surface((100, 150), pygame.SRCALPHA)
    surface.fill((0, 0, 0, 0))

    text_font = pygame.font.SysFont("Arial", 16, bold=True)
    score_font = pygame.font.SysFont("Arial", 40, bold=True)

    pygame.draw.rect(
        surface, theme.BOARD, pygame.Rect(0, 25, 100, 125), border_radius=10
    )
    draw_token(surface, 50, 25, 20, color)

    text_surface = text_font.render(text, True, (255, 255, 255))
    text_surface.convert_alpha()

    wins = score_font.render(str(score), True, (255, 255, 255))
    wins.convert_alpha()

    surface.blit(text_surface, ((100 - text_surface.get_width()) // 2, 50))
    surface.blit(wins, ((100 - wins.get_width()) // 2, 75))

    return surface


def button(text, width, height, highlight=False, fontSize=32):
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    surface.fill((0, 0, 0, 0))

    text_font = pygame.font.SysFont("Arial", fontSize, bold=True)

    color = theme.BOARD_HIGHLIGHT if highlight else theme.BOARD
    pygame.draw.rect(
        surface, color, pygame.Rect(0, 0, width, height), border_radius=15
    )

    text_surface = text_font.render(text, True, (255, 255, 255))
    text_surface.convert_alpha()

    surface.blit(
        text_surface,
        (
            (width - text_surface.get_width()) // 2,
            (height - text_surface.get_height()) // 2,
        ),
    )

    return surface


def draw_token(surface, x, y, radius, color):
    gfxdraw.aacircle(surface, x, y, radius, color[1])
    gfxdraw.filled_circle(surface, x, y, radius, color[1])

    gfxdraw.aacircle(surface, x, y, radius - 4, color[0])
    gfxdraw.filled_circle(surface, x, y, radius - 4, color[0])
