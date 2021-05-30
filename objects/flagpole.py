# FIX POLE

import pygame as pg

# Local imports
from characters.entity_constants import *
from game_setup import IMAGES, SOUND
from tools import scale_image

vec = pg.math.Vector2

class Pole(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.pos = vec(x, y)
        self.image = self.__get_image()
        self.rect = self.image.get_rect()
        self.rect.bottomright = self.pos
        self.mask = pg.mask.from_surface(self.image)

    def __get_image(self):
        return scale_image(IMAGES['pole'], FLAG_POLE_SCALAR)

    def update(self, *args):
        self.rect.bottomright = self.pos
        self.mask = pg.mask.from_surface(self.image)

class Flag(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.pos = vec(x, y)
        self.image = self.__get_image()
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos
        self.mask = pg.mask.from_surface(self.image)
        self.state = RESTING

    def __get_image(self):
        return scale_image(IMAGES['flag'], FLAG_POLE_SCALAR)  

    def update(self, player, *args):
        # mario is on pole
        if player.state == POLE_SLIDING:
            self.pos.y += 3
        self.rect.topleft = self.pos
        self.mask = pg.mask.from_surface(self.image)

class Finial(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.pos = vec(x, y)
        self.image = self.__get_image()
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.pos
        self.mask = pg.mask.from_surface(self.image)
        
    def __get_image(self):
        return scale_image(IMAGES['finial'], FLAG_POLE_SCALAR)

    def update(self, *args):
        self.rect.midbottom = self.pos
        self.mask = pg.mask.from_surface(self.image)
