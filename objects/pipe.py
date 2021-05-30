import pygame as pg

# Local imports
from tools import get_image, scale_image
from game_setup import IMAGES
from characters.entity_constants import *

# Pygame 2D Vector
vec = pg.math.Vector2


class Pipe(pg.sprite.Sprite):
    '''A class for a pipe'''
    def __init__(self, **kwargs):
        super().__init__()
        heights = { 'tall': TALL, 'short': SHORT }
        x = kwargs.get('x')
        y = kwargs.get('y', GROUND)
        self.height = heights[kwargs.get('height')]

        self.pos = vec(x, y)
        self.image = self.__get_image()
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.pos

    def __get_image(self):
        '''Returns an image based on the height value'''
        img = scale_image(IMAGES['pipe'], 0.45)

        if self.height == SHORT:    
            img = get_image(
                img, 0, 0, img.get_width(), 
                round(img.get_height() * 0.6)
            )
            
        return img

    def update(self):
        '''Updates the pipe'''
        self.rect.midbottom = self.pos
   