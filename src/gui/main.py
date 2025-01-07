from src.core.game import Game
import pygame

def main():
    game = Game()
    pygame.init()
    screen = pygame.display.set_mode([800, 500])
    screen.convert_alpha()
    pygame.display.set_caption("Connect 4")
    screen.fill((0,0,0))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.flip()
        pygame.time.Clock().tick(60)
    pygame.quit()

if __name__ == "__main__":
    main()
