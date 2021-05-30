'''General tool functions'''

from os import path, listdir

# Local imports
import pygame as pg
from pygame.transform import scale
from settings import *

def load_files(dir, type, accepted):
    '''Function for loading all files by type'''
    file_dict = {}
    for f in listdir(dir):
        name, ext = path.splitext(f)
        if ext.lower() in accepted:
            obj = None
            if type == 'image':
                obj = pg.image.load(path.join(dir, f))
                obj = obj.convert_alpha()
            elif type == 'sound':
                obj = pg.mixer.Sound(path.join(dir, f))
            elif type == 'music' or type == 'font' or type == 'data':
                obj = path.join(dir, f)
            if obj:
                file_dict[name] = obj

    return file_dict


def scale_image(img, scalar):
    '''Scales an image evenly by a specified factor'''
    return pg.transform.scale(
        img, 
        (
            round(img.get_width() * scalar),
            round(img.get_height() * scalar)
        )
    )


def get_image(spritesheet, x, y, width, height, scalar=None):
    '''Function that retrieves and returns an image from a sprite sheet'''
    # Creates a surface with the right dimensions
    img = pg.Surface((width, height)).convert_alpha()
    # Makes the surface transparent
    img.fill((0,0,0,0))
    # Blits the image from the sprite sheet on to the surface
    img.blit(spritesheet, (0,0), (x, y, width, height))

    if scalar:
        img = scale_image(img, scalar)

    return img
