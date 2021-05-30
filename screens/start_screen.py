import json

import pygame as pg


# Local imports
from tools import get_image, scale_image
from objects.ground_blocks import GroundBlock
from objects.pipe import Pipe
from game_setup import IMAGES, LOADING_SCREEN, WIDTH, WHITE, FONTS

class StartScreen:
    def __init__(self, file=None):
        self.next = LOADING_SCREEN
        self.running = True
        self.bg = IMAGES['background2']
        self.title_pic = IMAGES['title_pic_mario']
        self.block_pic =  pg.transform.scale(get_image(IMAGES['block-sheet'], 0, 0, 24, 24), (42, 42))
        self.mario_font  = pg.font.Font(FONTS['ARCADECLASSIC'], 34)
        self.start_label = self.mario_font.render('PRESS 1 TO START', 1, WHITE)
        self.highscore_label = self.mario_font.render('HIGHSCORE', 1, WHITE)
        self.mario_pic = pg.transform.scale2x(get_image(IMAGES['mario'], 176,  0, 16, 32))  
        self.brick_pic = pg.transform.scale(IMAGES['brick_64x64'], (42, 42))

        # Goomba
        width = height = 160
        self.goomba_pic = scale_image(get_image(IMAGES['goomba_sprites'], 120, 41, width, height), 0.2)

        self.ground_image = GroundBlock(x=0, width=WIDTH).image


    def __get_highscore(self):
        pass
    
    def start(self, *args):
        self.running = True

    def update(self, current_time, keys, **kwargs):
        if keys[pg.K_1]:
            self.running = False


    def draw(self, win):
        # Background
        win.fill((0, 0, 0))
        win.blit(self.bg, (0, 0))  

        # Labels
        win.blit(self.title_pic, (240, 100))  
        win.blit(self.start_label, (280, 300))
        win.blit(self.highscore_label, (280, 340))
        
        # Blocks
        win.blit(self.block_pic, (100, 400))
        win.blit(self.block_pic, (560, 400))
        win.blit(self.ground_image, (0, 540))
        win.blit(self.brick_pic, (604, 400))
        
        # Mario and enemies
        win.blit(self.mario_pic, (100, 476))
        win.blit(self.goomba_pic, (300, 506))

