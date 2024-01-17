import pygame, sys, random, time
from settings import *
from level import Level

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1440, 900))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("home away from home <3")
        self.level = Level() # creating attributes


    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            dt = self.clock.tick() / 1000
            self.level.run(dt)
            pygame.display.update()

if __name__ == '__main__': # checking if you are in the main file
    game = Game()
    game.run()
