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
        self.show_difficulty_modal = False
        self.difficulty_options = ["Easy", "Hard"]
        self.selected_difficulty = 0
        self.modal_rect = None

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

        if self.show_difficulty_modal:
            self.render_difficulty_modal()

    def render_difficulty_modal(self):
        s = pygame.Surface(
            (self.screen.get_width(), self.screen.get_height()), pygame.SRCALPHA
        )
        s.fill((0, 0, 0, 128))
        modal_width, modal_height = 300, 175
        modal_x = (self.screen.get_width() - modal_width) // 2
        modal_y = (self.screen.get_height() - modal_height) // 2
        self.modal_rect = pygame.Rect(modal_x, modal_y, modal_width, modal_height)

        pygame.draw.rect(
            s,
            theme.BACKGROUND,
            self.modal_rect,
            border_radius=10,
        )

        pygame.draw.rect(
            s,
            theme.BOARD_HIGHLIGHT,
            self.modal_rect,
            2,
            border_radius=10,
        )

        for i, option in enumerate(self.difficulty_options):
            highlight = i == self.selected_difficulty
            button_surface = button(option, 200, 50, highlight)
            rect = button_surface.get_rect(
                center=(self.screen.get_width() // 2, modal_y + 50 + i * 75)
            )
            s.blit(button_surface, rect)

        self.screen.blit(s, (0, 0))

    def handle_event(self, event):
        if self.show_difficulty_modal:
            self.handle_difficulty_modal_event(event)
        else:
            self.handle_main_menu_event(event)

    def handle_main_menu_event(self, event):
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

    def handle_difficulty_modal_event(self, event):
        match event.type:
            case pygame.KEYDOWN:
                match event.key:
                    case pygame.K_UP:
                        self.selected_difficulty = (self.selected_difficulty - 1) % len(
                            self.difficulty_options
                        )
                    case pygame.K_DOWN:
                        self.selected_difficulty = (self.selected_difficulty + 1) % len(
                            self.difficulty_options
                        )
                    case pygame.K_RETURN:
                        self.start_game_with_difficulty()
                    case pygame.K_ESCAPE:
                        self.show_difficulty_modal = False
            case pygame.MOUSEMOTION:
                pos = event.pos
                hovered = False
                for i in range(len(self.difficulty_options)):
                    rect = pygame.Rect(
                        (
                            self.screen.get_width() // 2 - 100,
                            self.screen.get_height() // 2 - 50 + i * 75,
                        ),
                        (200, 50),
                    )
                    if rect.collidepoint(pos):
                        self.selected_difficulty = i
                        hovered = True
                if not hovered:
                    self.selected_difficulty = -1
            case pygame.MOUSEBUTTONUP:
                pos = event.pos
                if not self.modal_rect.collidepoint(pos):
                    self.show_difficulty_modal = False
                else:
                    for i in range(len(self.difficulty_options)):
                        rect = pygame.Rect(
                            (
                                self.screen.get_width() // 2 - 100,
                                self.screen.get_height() // 2 - 50 + i * 75,
                            ),
                            (200, 50),
                        )
                        if rect.collidepoint(pos):
                            self.selected_difficulty = i
                            self.start_game_with_difficulty()

    def handle_selection(self):
        match self.selected_option:
            case 0:
                self.scene_manager.switch_scene("GameScene", playWithBot=False)
            case 1:
                self.show_difficulty_modal = True
            case 2:
                pygame.quit()
                sys.exit()

    def start_game_with_difficulty(self):
        self.show_difficulty_modal = False
        difficulty = self.difficulty_options[self.selected_difficulty]
        bot_algorithm = "rand" if difficulty == "Easy" else "minimax"
        self.scene_manager.switch_scene(
            "GameScene",
            playWithBot=True,
            botAlgorithm=bot_algorithm,
        )
