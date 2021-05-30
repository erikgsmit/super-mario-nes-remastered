import pygame as pg

# Local imports
from game_setup import FONTS
from settings import WHITE

# Pygame 2D Vector
vec = pg.math.Vector2


class ScoreLabel:
    '''A class for a floating score label'''
    def __init__(self, value, x, y):
        self.font = pg.font.Font(FONTS['ARCADECLASSIC'], 16)
        self.value = value
        self.start_timer = pg.time.get_ticks()
        self.pos = vec(x, y)
        self.text = self.font.render(self.value, 1, WHITE)
        self.is_active = True

    def update(self):
        '''Updates the label's position'''
        self.pos.y -= 2
        self.text = self.font.render(self.value, 1, WHITE)

    def draw(self, win):
        '''Draws the label on to the screen'''
        win.blit(self.text, (self.pos.x, self.pos.y))
