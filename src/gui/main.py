import pygame

from src.gui.gameScene import GameScene
from src.gui.mainMenuScene import MainMenuScene
from src.gui.sceneManager import SceneManager

pygame.init()
pygame.font.init()
pygame.display.set_caption("Connect 4")

screen = pygame.display.set_mode((800, 500))
screen.convert_alpha()

scene_manager = SceneManager(screen)

main_menu_scene = MainMenuScene(screen, scene_manager)
scene_manager.add_scene("MainMenuScene", main_menu_scene)

connect4_scene = GameScene(screen, scene_manager)
scene_manager.add_scene("NewGameScene", connect4_scene)

scene_manager.switch_scene("MainMenuScene")

while True:
    scene_manager.run_current_scene()
    pygame.display.flip()
