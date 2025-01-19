import sys

import pygame

import src.gui.theme as theme
from src.gui.gameScene import button, draw_token


class MainMenuScene:
    def __init__(self, screen, scene_manager):
        self.screen = screen
        self.scene_manager = scene_manager
        self.font = pygame.font.Font(None, 72)

        self.title_text = self.font.render("Connect 4", True, (255, 255, 255))
        self.title_rect = self.title_text.get_rect()

        self.menu_options = ["Player vs Player", "Player vs Bot", "Quit"]
        self.selected_option = 0

    def setup(self):
        pass

    def cleanup(self):
        pass

    def update(self):
        pass

    def render(self):
        self.screen.fill(theme.BACKGROUND)

        token_radius = 15
        token_spacing = 5
        logo_width = token_radius * 4 + token_spacing * 3
        total_width = self.title_rect.width + logo_width + 20

        self.title_rect.center = (
            self.screen.get_width() // 2
            - total_width // 2
            + self.title_rect.width // 2,
            100,
        )
        logo_x = self.title_rect.right + 20
        logo_y = self.title_rect.centery

        self.screen.blit(self.title_text, self.title_rect)

        draw_token(
            self.screen,
            logo_x,
            logo_y - token_radius - token_spacing // 2,
            token_radius,
            theme.YELLOW,
        )
        draw_token(
            self.screen,
            logo_x + token_radius * 2 + token_spacing,
            logo_y - token_radius - token_spacing // 2,
            token_radius,
            theme.RED,
        )
        draw_token(
            self.screen,
            logo_x,
            logo_y + token_radius + token_spacing // 2,
            token_radius,
            theme.RED,
        )
        draw_token(
            self.screen,
            logo_x + token_radius * 2 + token_spacing,
            logo_y + token_radius + token_spacing // 2,
            token_radius,
            theme.YELLOW,
        )

        for i, option in enumerate(self.menu_options):
            highlight = i == self.selected_option
            button_surface = button(option, 300, 50, highlight)
            rect = button_surface.get_rect(
                center=(self.screen.get_width() // 2, 200 + i * 75)
            )
            self.screen.blit(button_surface, rect)

    def handle_event(self, event):
        match event.type:
            case pygame.KEYDOWN:
                match event.key:
                    case pygame.K_UP:
                        self.selected_option = (self.selected_option - 1) % len(
                            self.menu_options
                        )
                    case pygame.K_DOWN:
                        self.selected_option = (self.selected_option + 1) % len(
                            self.menu_options
                        )
                    case pygame.K_RETURN:
                        self.handle_selection()
            case pygame.MOUSEMOTION:
                pos = event.pos
                hovered = False
                for i in range(len(self.menu_options)):
                    rect = pygame.Rect(
                        (self.screen.get_width() // 2 - 100, 200 + i * 75 - 25),
                        (200, 50),
                    )
                    if rect.collidepoint(pos):
                        self.selected_option = i
                        hovered = True
                if not hovered:
                    self.selected_option = -1
            case pygame.MOUSEBUTTONUP:
                pos = event.pos
                for i in range(len(self.menu_options)):
                    rect = pygame.Rect(
                        (self.screen.get_width() // 2 - 100, 200 + i * 75 - 25),
                        (200, 50),
                    )
                    if rect.collidepoint(pos):
                        self.selected_option = i
                        self.handle_selection()

    def handle_selection(self):
        match self.selected_option:
            case 0:
                self.scene_manager.switch_scene(
                    "NewGameScene", playWithBot=False
                )
            case 1:
                self.scene_manager.switch_scene(
                    "NewGameScene", playWithBot=True
                )
            case 2:
                pygame.quit()
                sys.exit()
