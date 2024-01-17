import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, position, group):
        super().__init__(group)

        self.image = pygame.Surface((16,16))
        self.image.fill('pink')
        self.rect = self.image.get_rect(center = position)


        #movement attributres
        self.direction = pygame.math.Vector2()
        self.position = pygame.math.Vector2(self.rect.center)
        self.speed = 200

    def import_assets(self):
        self.animations = {'up': [], 'down': [], }

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.direction.y = -1
            print('up')
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
            print('down')
        else:
            self.direction.y = 0
        
        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            print('right')
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            print('left')
        else:
            self.direction.x = 0

    def move(self, dt):
        #normalize the vector
        if self.direction.magnitude > 0:
            self.direction = self.direction.normalize()
        
        #horizontal movement
        self.position.x += self.direction.x * self.speed * dt
        self.rect.centerx = self.position.x

        #vertical movement
        self.position.y += self.direction.y * self.speed * dt
        self.rect.centery = self.position.y

    def update(self, dt):
        self.input()
        self.move(dt)
