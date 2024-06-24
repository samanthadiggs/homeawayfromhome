import pygame
from settings import *
from random import randint, choice
from timer import Timer

class Generic(pygame.sprite.Sprite):
    def __init__(self, pos, surface, groups, z = LAYERS['main']):
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_rect(topleft = pos)
        self.z = z
        self.hitbox= self.rect.copy().inflate(-self.rect.width*0.2, -self.rect.height*0.75)

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
        self.hitbox = self.rect.copy().inflate(-20, -self.rect.height*0.9)

class Tree(Generic):
    def __init__(self, pos, surface, groups, name):
        super().__init__(pos, surface, groups)

        #tree attributes
        self.health = 5
        self.alive = True
        stump_path = f'/Users/samanthadiggs/Desktop/code/homeawayfromhome/assets/graphics/stumps/{"small" if name == "Small" else "large"}.png'
        self.stump_surface = pygame.image.load(stump_path).convert_alpha() #what the tree looks like if the tree is dead
        self.invul_timer = Timer(200)


        # apples for trees
        self.apples_surface = pygame.image.load('/Users/samanthadiggs/Desktop/code/homeawayfromhome/assets/graphics/fruit/apple.png')
        self.apple_position = APPLE_POSITION[name]
        self.apple_sprites = pygame.sprite.Group()
        self.create_fruit()

    def damage(self):
        #damaging the tree
        self.health -= 1

        #remove an apple
        if len(self.apple_sprites.sprites()) > 0:
            random_apple = choice(self.apple_sprites.sprites())
            random_apple.kill()
    
#def 

    def create_fruit(self):
        for position in self.apple_position:
            if randint(0,10) < 2:
                x = position[0] + self.rect.left # the left side of the tree
                y = position[1] + self.rect.top 
                Generic(
                    pos = (x,y),
                    surface = self.apples_surface,
                    groups = [self.apple_sprites, self.groups()[0]], #calling the first element from the groups list that is all the groups the Tree is in. 
                    z = LAYERS['fruit']
                )
                print("apple has been created")
