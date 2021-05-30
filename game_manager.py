from settings import START_SCREEN
from game_setup import *
from screens.game_over_screen import GameOverScreen
from screens.start_screen import StartScreen
from screens.loading_screen import LoadingScreen
from screens.level1 import Level1
from characters.mario import Player

class GameManager:
    '''Manages the different game screens and contains the game loop'''
    def __init__(self):
        self.win = WIN
        self.clock = pg.time.Clock()
        self.running = True
        self.current_time = 0
        self.keys = pg.key.get_pressed()
        self.player = Player()
        self.screen_dict = {
            START_SCREEN: StartScreen(),
            LOADING_SCREEN: LoadingScreen(),
            GAME_OVER_SCREEN: GameOverScreen(),
            LEVEL_SCREEN: Level1(self.player)
        }
        self.screen = self.screen_dict[START_SCREEN]

    def set_level(self, level):
        '''Called when user selects level'''
        if level == LEVEL_1:
            self.screen_dict[LEVEL_SCREEN] = Level1()

    def run(self):
        '''Runs the game loop'''
        while self.running:
            self.__events()
            self.__update()
            self.__draw()
            self.clock.tick(FPS)
            pg.display.set_caption(f'{TITLE}  {round(self.clock.get_fps(), 3)} FPS')

    def __events(self):
        '''Checks events'''
        for event in pg.event.get():
            # Check for closing window
            if event.type == pg.QUIT:
                self.running = False
            elif event.type == pg.KEYDOWN:
                self.keys = pg.key.get_pressed()
            elif event.type == pg.KEYUP:
                self.keys = pg.key.get_pressed()

    def __update(self):
        self.current_time = pg.time.get_ticks()

        # Check to switch screen
        if not self.screen.running:
            self.screen = self.screen_dict[self.screen.next]
            self.screen.start(self.current_time) 
        
        self.screen.update(self.current_time, self.keys, player_lives=self.player.lives)

    def __draw(self):
        self.screen.draw(self.win)
        pg.display.update()

def main():
    g = GameManager()
    g.run()
            
    pg.quit()


if __name__ == '__main__':
    main() 

