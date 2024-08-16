import pygame
from sys import exit
from constantes import *
from classes import *


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.screen_config()
        self.loop()
    
    def screen_config(self) -> None:
        self.screen = pygame.display.set_mode((LARGURA, ALTURA))
        pygame.display.set_caption('ADGP')
        self.clock = pygame.time.Clock()
    
    def loop(self) -> None:
        level = Level(self.screen)

        while True:
            self.screen.fill((235, 235, 235)) # Temporário
            self.clock.tick(FPS)

            self.eventos()

            level.run()     

            pygame.display.flip()

    def eventos(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()


if __name__ == '__main__':
    Game()
