import pygame
from settings import *
from player import Player
from overlay import Overlay
from sprites import Generic, Water, WildFlower, Tree
from pytmx.util_pygame import load_pygame
from support import *
class Level:
    def __init__(self):

        # get display surface
        self.display_surface = pygame.display.get_surface() # the same as self.screen, alllows the level to draw straight on the display

        # sprite groups
        self.all_sprites = CameraGroup()
        self.collision_sprites = pygame.sprite.Group() #keeping track of sprites that can be collided with
        self.tree_sprites = pygame.sprite.Group()

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

        # house pt 2
        for layer in ['HouseWalls', 'HouseFurnitureTop']:
            for x,y, surface in tmx_data.get_layer_by_name(layer).tiles():
                Generic(
                    pos = (x * TILE_SIZE, y*TILE_SIZE), 
                    surface = surface, 
                    groups = self.all_sprites, 
                    z = LAYERS['main'])

        # fence
        for x,y,surface in tmx_data.get_layer_by_name("Fence").tiles():
            Generic(
                pos = (x * TILE_SIZE, y*TILE_SIZE), 
                surface = surface, 
                groups = [self.all_sprites, self.collision_sprites ], 
                z = LAYERS['main'])
        #water
        water_frames = import_folder('assets/graphics/water')
        for x,y,surface in tmx_data.get_layer_by_name("Water").tiles():
            Water(pos = (x * TILE_SIZE, y*TILE_SIZE), 
                frames = water_frames, 
                groups = self.all_sprites, 
                z = LAYERS['main'])
        #trees
        for objects in tmx_data.get_layer_by_name("Trees"):
            Tree(
                pos = (objects.x, objects.y), 
                surface = objects.image, 
                groups= [self.all_sprites, self.collision_sprites, self.tree_sprites], 
                name = objects.name)
        
        #wildflower
        for objects in tmx_data.get_layer_by_name("Decoration"):
            WildFlower(
                pos = (objects.x, objects.y), 
                surface = objects.image, 
                groups = [self.all_sprites, self.collision_sprites], )
        
        #collision map
        for x, y, surface in tmx_data.get_layer_by_name("Collision").tiles():
            Generic(
                pos = (x* TILE_SIZE, y*TILE_SIZE),
                surface = pygame.Surface((TILE_SIZE, TILE_SIZE)),
                groups = self.collision_sprites #will not be drawn or updated
            )
        # Player
        for object in tmx_data.get_layer_by_name("Player"):
            if object.name == "Start":
                self.player = Player(
                    position=(object.x, object.y), 
                    group= self.all_sprites, 
                    collision_sprites=self.collision_sprites,
                    tree_sprites=self.tree_sprites) #player sprite itself is not in collision sprites group
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
            for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
                if sprite.z == layer:
                    offset_rect = sprite.rect.copy()
                    offset_rect.center -= self.offset
                    self.display_surface.blit(sprite.image, offset_rect)

                """ 
                if sprite == player:
                        pygame.draw.rect(self.display_surface, 'red', offset_rect, 5)
                        hitbox_rect = player.hitbox.copy()
                        hitbox_rect.center = offset_rect.center
                        pygame.draw.rect(self.display_surface, 'green', hitbox_rect, 5)
                        target_pos = offset_rect.center + PLAYER_TOOL_OFFSET[player.status.split('_')[0]]
                        pygame.draw.circle(self.display_surface, 'blue', target_pos, 5) """