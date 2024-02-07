import pygame
from settings import *
from player import Player
from overlay import Overlay
from sprites import Generic
from pytmx.util_pygame import load_pygame
class Level:
    def __init__(self):

        # get display surface
        self.display_surface = pygame.display.get_surface() # the same as self.screen, alllows the level to draw straight on the display

        # sprite groups
        self.all_sprites = CameraGroup()

        self.setup()
        self.overlay = Overlay(self.player)

    def setup(self):
        tmx_data = load_pygame('assets/data/hafh_custom_map.tmx')

        # house
        for layer in ['HouseFloor', 'HouseFurnitureBottom']:
            for x,y, surface in tmx_data.get_layer_by_name(layer).tiles():
                Generic(
                    pos = (x * TILE_SIZE, y*TILE_SIZE), 
                    surface = surface, 
                    groups = self.all_sprites, 
                    z = LAYERS['house bottom'])


        self.player = Player((640, 360), self.all_sprites)
        Generic(
            pos = (0,0),
            surface = pygame.image.load('assets/graphics/world/ground.png').convert_alpha(),
            groups = self.all_sprites,
            z = LAYERS['ground']
        )
    def run(self, dt):
        self.display_surface.fill('black')
        #self.all_sprites.draw(self.display_surface)
        self.all_sprites.custom_draw(self.player)
        self.all_sprites.update(dt)
        self.overlay.display()

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()

    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - SCREEN_WIDTH / 2
        self.offset.y = player.rect.centery - SCREEN_HEIGHT / 2 #ensures that the player is in the center of the camera



        for layer in LAYERS.values():
            for sprite in self.sprites():
                if sprite.z == layer:
                    offset_rect = sprite.rect.copy()
                    offset_rect.center -= self.offset
                    self.display_surface.blit(sprite.image, offset_rect)

