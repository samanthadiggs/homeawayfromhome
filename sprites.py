import pygame
from settings import *

class Generic(pygame.sprite.Sprite):
    def __init__(self, pos, surface, groups, z = LAYERS['main']):
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_rect(topleft = pos)
        self.z = z

class Water(Generic):
    def __init__(self, pos, frames, groups, z):

        #animation setup
        self.frames = frames
        self.frame_index = 0

        # sprite setup
        super().__init__(
            pos = pos, 
            surface = self.frames[self.frame_index], 
            groups = groups, 
            z = LAYERS['water'])
        
    def animate(self, dt):
        self.frame_index += 4 * dt
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def update(self,dt):
        self.animate(dt)

class WildFlower(Generic):
    def __init__(self, pos, surface, groups):
        super().__init__(pos, surface, groups)

class Tree(Generic):
    def __init__(self, pos, surface, groups, name):
        super().__init__(pos, surface, groups)