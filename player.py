import pygame
from settings import *
from support import import_folder
from timer import Timer

class Player(pygame.sprite.Sprite):
    def __init__(self, position, group):
        super().__init__(group)

        #managing assets
        self.import_assets()
        self.status = 'down_idle'
        self.frame_index = 0

        # general setup
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center = position)
        self.z = LAYERS['main']

        #managing tools
        self.tools = ['hoe', 'axe', 'water']
        self.tool_index = 0
        self.selected_tool = self.tools[self.tool_index]

        #s seeds
        self.seeds = ['corn', 'tomato']
        self.seed_index = 0
        self.selected_seed = self.seeds[self.seed_index]        

        #movement attributres
        self.direction = pygame.math.Vector2()
        self.position = pygame.math.Vector2(self.rect.center)
        self.speed = 200

        #timers
        self.timers = {
            'tool use':Timer(350, self.use_tool),
            'tool switch':Timer(200),
            'seed use': Timer(350, self.use_seed),
            'seed switch': Timer(200)
        }

    def use_tool(self):
        pass
        #print(self.selected_tool)
    
    def use_seed(self):
        pass
    def import_assets(self):
        self.animations = {'up': [], 'down': [], 'right':[], 'left':[],
                           'up_idle': [], 'down_idle': [], 'right_idle':[], 'left_idle':[],
                           'up_hoe': [], 'down_hoe': [], 'right_hoe':[], 'left_hoe':[],
                           'up_axe': [], 'down_axe': [], 'right_axe':[], 'left_axe':[],
                           'up_water': [], 'down_water': [], 'right_water':[], 'left_water':[]}
        for animation in self.animations.keys():
            full_path = 'assets/graphics/character/' + animation
            self.animations[animation] = import_folder(full_path)
        print(self.animations)

    def animate(self, dt):
        self.frame_index += 4 * dt
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0

        self.image = self.animations[self.status][int(self.frame_index)]

    def input(self):
        keys = pygame.key.get_pressed()
        if not self.timers['tool use'].active: #cannot do anything else while a tool is being used
            #directions
            if keys[pygame.K_UP]:
                self.direction.y = -1
                self.status = "up"
                print('up')
            elif keys[pygame.K_DOWN]:
                self.direction.y = 1
                self.status = "down"
                print('down')
            else:
                self.direction.y = 0
            
            if keys[pygame.K_RIGHT]:
                self.direction.x = 1
                self.status = "right"
                print('right')
            elif keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.status = "left"
                print('left')
            else:
                self.direction.x = 0
            
            #tool use
            if keys[pygame.K_SPACE]:
                #timer for the tool use
                self.timers['tool use'].activate()
                self.direction = pygame.math.Vector2()
                self.frame_index = 0 #want to play the first frame of the animation when you use a tool

            #change tools
            if keys[pygame.K_q] and not self.timers['tool switch'].active:
                self.timers['tool switch'].activate()
                self.tool_index += 1
                if self.tool_index < len(self.tools):
                    self.tool_index = self.tool_index
                else:
                    self.tool_index = 0
                self.selected_tool = self.tools[self.tool_index]
            
            #seed use
            if keys[pygame.K_1]:
                self.timers['seed use'].activate()
                self.direction = pygame.math.Vector2()
                self.frame_index = 0 #want to play the first frame of the animation when you use a tool
                print('use seed')
            #change seed
            if keys[pygame.K_2] and not self.timers['seed switch'].active:
                self.timers['seed switch'].activate()
                self.seed_index += 1
                if self.seed_index < len(self.seeds):
                    self.seed_index = self.seed_index
                else:
                    self.seed_index = 0
                self.selected_seed = self.seeds[self.seed_index]



    def get_status(self):
        # check if player is not moving

        if self.direction.magnitude() == 0:
            self.status = self.status.split('_')[0] + "_idle"
        
        if self.timers['tool use'].active:
            print('tool is being used')
            self.status = self.status.split("_")[0] + "_" + self.selected_tool
    
    def update_timers(self):
        for timer in self.timers.values():
            timer.update()

    def move(self, dt):
        #normalize the vector
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()
        
        #horizontal movement
        self.position.x += self.direction.x * self.speed * dt
        self.rect.centerx = self.position.x

        #vertical movement
        self.position.y += self.direction.y * self.speed * dt
        self.rect.centery = self.position.y

    def update(self, dt):
        self.input()
        self.get_status()
        self.update_timers()

        self.move(dt)
        self.animate(dt)
