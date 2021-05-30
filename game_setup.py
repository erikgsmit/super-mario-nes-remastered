'''Initializes pygame and loads resources'''

import pygame as pg

# Local imports
from settings import *
from tools import load_files

# Initialize pygame
pg.mixer.pre_init(44100, -16, 2, 2048)
pg.mixer.init()
pg.font.init()
pg.init()

# Events
pg.event.set_allowed([pg.KEYDOWN, pg.KEYUP, pg.QUIT])

# Display
WIN = pg.display.set_mode(SCREEN_SIZE)
pg.display.set_caption(TITLE)

# Load files
IMAGES = load_files(IMAGE_PATH, 'image', ('.png', '.jpg'))
SOUND  = load_files(SOUND_PATH, 'sound', ('.wav', '.ogg', '.mdi'))
MUSIC  = load_files(MUSIC_PATH, 'music', ('.wav', '.ogg', '.mdi', '.mp3'))
FONTS  = load_files(FONTS_PATH, 'font', ('.ttf'))
DATA   = load_files(DATA_PATH, 'data', ('.json'))

# Set icon
pg.display.set_icon(IMAGES['icon'])
