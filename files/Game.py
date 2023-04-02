import pygame
from .misc.settings import *
from .screens.Level import Level


class Game:
    def __init__(self) -> None:
        pygame.init()
        
        pygame.display.set_caption('Solitaire')
        
        self.screen = pygame.display.set_mode([WIDTH, HEIGHT])
        self.clock = pygame.time.Clock()
    
    def run(self):
        level = Level(self.screen, self.clock)
        level.run()

        pygame.quit()
        