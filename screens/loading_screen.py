import pygame as pg

# Local imports
from settings import LEVEL_SCREEN
from game_setup import *
from tools import get_image, scale_image

class LoadingScreen:
    def __init__(self):
        self.next = LEVEL_SCREEN
        self.running = True
        self.mario_font  = pg.font.Font(FONTS['ARCADECLASSIC'], 34)
        self.mario_label = self.mario_font.render('MARIO', 1, WHITE)
        self.score_label = self.mario_font.render('000000', 1, WHITE)
        self.coin_label = self.mario_font.render('x 00', 1, WHITE)
        self.time_label = self.mario_font.render('TIME', 1, WHITE)
        self.world_label = self.mario_font.render('WORLD', 1, WHITE)
        self.level_label = self.mario_font.render('1x1', 1, WHITE)
        self.x_label = self.mario_font.render('x', 1, WHITE)
        self.lives_label = self.mario_font.render('2', 1, WHITE)
        self.mario_pic = self.mario_pic = pg.transform.scale2x(get_image(IMAGES['mario'], 176, 0, 16, 32))  
        self.coin_pic = pg.transform.scale(IMAGES['label_coin'],(26,26))

        # loading coin
        self.spritesheet = IMAGES['coin_sheet']
        self.count = 0
        self.loading_image =  get_image(self.spritesheet, 147, 150, 62, 61)

        self.images = self.__load_images()
        
    def __load_images(self):
        '''Loads images and returns them as a list'''
        start_x = 147
        start_y = 150
        width = 62
        height = 61

        images = []
        # Appends all necessary images from the sprite sheet to the images list
        for i in range(6):
            x = start_x + i*(width)
            y = start_y
            images.append(scale_image(get_image(self.spritesheet, x, y, width, height), 0.4))

        return images 
          
    def start(self, current_time):
        self.start_time = current_time
        self.running = True
    
    def __update_image(self):
        '''Animates between images'''
        self.loading_image = self.images[(self.count // 3) % len(self.images)]
        self.rect = self.loading_image.get_rect()
        self.count += 1

    def update(self, current_time, *args, **kwargs):
        self.__update_image()
        lives = kwargs.get('player_lives')
        self.lives_label = self.mario_font.render(str(lives), 1, WHITE)
        if current_time - self.start_time > 3000:
            self.running = False

    def draw(self, win):
        win.fill((0,0,0))
        
        # Draw labels
        win.blit(self.mario_label, (70, 16))
        win.blit(self.score_label, (70, 40))
        win.blit(self.coin_label, (260, 40))
        win.blit(self.world_label,(410,16))
        win.blit(self.level_label,(420,40))
        win.blit(self.time_label,(600,16))

        win.blit(self.world_label,(300,200))
        win.blit(self.level_label,(420,200))
        win.blit(self.x_label,(390,320))
        win.blit(self.lives_label,(470,320))

        # Pictures
        win.blit(self.coin_pic,(230,44))
        win.blit(self.mario_pic,(300,300))

        # Loading image
        win.blit(self.loading_image,(720,550))
