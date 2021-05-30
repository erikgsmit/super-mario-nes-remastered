import pygame as pg

# Local imports
from settings import BLACK
from characters.entity_constants import GROUND
from game_setup import IMAGES
from tools import get_image

# Pygame 2D Vector
vec = pg.math.Vector2


class GroundBlock(pg.sprite.Sprite):
    '''A class for a ground block'''
    def __init__(self, **kwargs):
        super().__init__()
        x = kwargs.get('x')
        width = kwargs.get('width')

        self.pos = vec(x, GROUND)
        self.image = self.__get_image(width)
        self.rect = self.image.get_rect()

    def __get_image(self, width):
        '''Creates a pygame surface and adds ground images to it to fill the entire width'''
        img = pg.Surface((width, 73))
        img_piece = get_image(IMAGES['ground-blocks'], 48, 0, 144, 73)
        piece_width = 144
        c = 0
        x = width
        while x > 0:
            t = piece_width
            if x < piece_width: t = x
            img.blit(
                img_piece, (c * piece_width, 0), 
                (0, 0, t, 73)
            )
            x -= piece_width
            c += 1

        img.set_colorkey(BLACK)

        return img

    def update(self):
        self.rect.topleft = self.pos
