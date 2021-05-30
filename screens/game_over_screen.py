
# Local imports
from settings import START_SCREEN
from game_setup import *
from tools import get_image

class GameOverScreen:
    def __init__(self):
        self.next = START_SCREEN
        self.running = True
        self.mario_font  = pg.font.Font(FONTS['ARCADECLASSIC'], 34)
        self.game_over_label = self.mario_font.render("GAME OVER",1,WHITE)
 
    def start(self, current_time):
        self.start_time = current_time
        self.running = True

    def update(self, current_time, *args, **kwargs):
        if current_time - self.start_time > 3000:
            self.running = False

    def draw(self, win):
        win.fill((0,0,0))
        win.blit(self.game_over_label,(300,200))
     