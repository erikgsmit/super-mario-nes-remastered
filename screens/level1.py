import json

import pygame as pg

# Local imports
from game_setup import IMAGES, DATA, FONTS
from settings import WHITE, WIDTH, LOADING_SCREEN, GAME_OVER_SCREEN
from objects.blocks import QuestionBox, Brick
from objects.pipe import Pipe
from objects.ground_blocks import GroundBlock
from objects.flagpole import Pole, Flag, Finial
from characters.enemies import Goomba
from characters.entity_constants import *
from powerups.powerup_states import OPENED

class Level1:
    '''A class for the first level'''
    def __init__(self, player):
        super().__init__()
        self.lives_left = STARTING_LIVES
        self.player = player
        self.player_group = pg.sprite.Group(self.player)
        
        self.start()

    def start(self, *args):
        self.bg_x = 0
        self.death_timer = 0
       
        self.next = LOADING_SCREEN
        self.running = True

        self.level_data = DATA['level1']
        self.time_limit = 300
        self.time_stamp = 0
        self.bg = IMAGES['background2']
        
        self.player.reset()

        # Initially empty sprite groups
        self.brick_pieces = pg.sprite.Group()
        self.powerups = pg.sprite.Group()
        self.fireballs = pg.sprite.Group()
        
        self.__load_level_objects()
        self.__setup_labels()
        self.coin_pic = pg.transform.scale(IMAGES['label_coin'], (26, 26))

    def __load_level_objects(self):
        '''Loads all sprite objects from level_data'''
        with open(self.level_data) as f:
            data = json.load(f)

        self.ground_blocks = pg.sprite.Group(*[GroundBlock(**block) for block in data['ground-blocks']])
        self.pipes = pg.sprite.Group(*[Pipe(**pipe) for pipe in data['pipes']])
        self.enemies = pg.sprite.Group(*[Goomba(**goomba) for goomba in data['goombas']])
        self.boxes = pg.sprite.Group(
            *[QuestionBox(self.powerups, **box) for box in data['q-boxes']],
            *[Brick(self.powerups, self.brick_pieces, **brick) for brick in data['bricks']]
        )

        def flagpole(right_x):
            pole = Pole(right_x, GROUND)
            block_x = right_x - (pole.image.get_width() / 2) - 21
            block = QuestionBox(self.powerups, x=block_x, y=GROUND-42)
            block.state = OPENED
            block.image = block.opened
            y_flag = GROUND - pole.image.get_height()
            flag = Flag(right_x, y_flag)
            x_finial = right_x - pole.image.get_width() / 2
            finial = Finial(x_finial, GROUND - pole.image.get_height())

            return pg.sprite.Group(pole, flag, finial, block)

        self.flagpole = flagpole(data['flagpole']['x'])

        self.non_player_sprites = pg.sprite.Group(
            self.boxes, 
            self.enemies, 
            self.ground_blocks, 
            self.pipes, 
            self.flagpole
        )

    def __setup_labels(self):
        self.mario_font = pg.font.Font(FONTS['ARCADECLASSIC'], 34)
        self.mario_label = self.mario_font.render('MARIO', 1, WHITE)
        self.score_label = self.mario_font.render('000000', 1, WHITE)
        self.coin_label = self.mario_font.render('x 00', 1, WHITE)
        self.time_label = self.mario_font.render('TIME', 1, WHITE)
        self.time_limit_label = self.mario_font.render('300', 1, WHITE)
        self.world_label = self.mario_font.render('WORLD', 1, WHITE)
        self.level_label = self.mario_font.render('1x1', 1, WHITE)
        self.labels = []        

    def __check_time_limit(self, current_time):
        if current_time-self.time_stamp >= 1000:
            self.time_stamp = current_time
            self.time_limit -= 1
            self.time_limit_label = self.mario_font.render(str(self.time_limit), 1, WHITE)
        
        if self.time_limit == 0:
            self.player.lives -= 1

    def __check_lives(self):
        if self.player.lives < self.lives_left:
            if self.player.lives <= 0:
                self.next = GAME_OVER_SCREEN
                self.player.lives = STARTING_LIVES
            else:
                self.next = LOADING_SCREEN
            self.lives_left = self.player.lives
            self.running = False

    def update(self, current_time, keys, **kwargs):
        '''Updates everything'''
        self.__move_screen()
        
        self.enemies.update(current_time, self.boxes, self.pipes, self.ground_blocks)
        self.player_group.update(
            current_time, keys, self.labels, self.flagpole, self.powerups, self.boxes, self.pipes, 
            self.ground_blocks, self.enemies
        )
        self.fireballs = self.player.fireballs
        self.fireballs.update(self.player, self.labels, self.boxes, self.ground_blocks, self.pipes, self.enemies)
        self.boxes.update(self.player)
        self.pipes.update()
        self.ground_blocks.update()
        self.brick_pieces.update()
        self.flagpole.update(self.player)
        self.powerups.update(self.labels, self.boxes, self.ground_blocks, self.pipes)
        self.__update_labels(current_time)
        self.__check_time_limit(current_time)
        self.__check_lives()

    def draw(self, win):
        '''Draws everything on screen'''
        def redraw_window(win):
            win.fill((0, 0, 0))
            win.blit(self.bg, (self.bg_x, 0))  
            win.blit(self.coin_pic, (230, 44))

        def draw_labels(win):
            win.blit(self.mario_label, (70, 16))
            win.blit(self.score_label, (70, 40))
            win.blit(self.coin_label, (260, 40))
            win.blit(self.world_label, (410, 16))
            win.blit(self.level_label, (420, 40))
            win.blit(self.time_label, (600, 16))
            win.blit(self.time_limit_label, (610, 40))
        
            for l in self.labels:
                l.draw(win)

        redraw_window(win)
        self.ground_blocks.draw(win)
        self.brick_pieces.draw(win)
        self.powerups.draw(win)
        self.fireballs.draw(win)
        self.boxes.draw(win)
        self.pipes.draw(win)
        self.enemies.draw(win)
        self.player_group.draw(win)
        self.flagpole.draw(win)
        draw_labels(win)

    def __update_labels(self, current_time):
        '''Updates all the text labels on screen'''
        def update_floating_labels():
            i = 0
            while i < len(self.labels):
                self.labels[i].update()
                if current_time - self.labels[i].start_timer > 1000:
                    del self.labels[i]
                else:
                    i += 1
        
        score_text = str(self.player.score)
        zeros = 6 - len(score_text)  # Number of zeros before the actual score
        score_text = '0'*zeros + score_text
        self.score_label = self.mario_font.render(score_text, 1, WHITE)

        # Coin label
        coin_text = str(self.player.coins)
        zeros = 2 - len(coin_text)  # Number of zeros before the actual score
        coin_text = 'x0'*zeros + coin_text
        self.coin_label = self.mario_font.render(coin_text, 1, WHITE)

        update_floating_labels()

    def __move_screen(self):
        '''Adjusts the position of all elements based on marios x movement'''
        if self.player.rect.centerx >= WIDTH/2:
            self.player.pos.x = WIDTH/2
            for entity in self.non_player_sprites:
                entity.pos.x -= self.player.vel.x
            for entity in self.powerups:
                entity.pos.x -= self.player.vel.x
            for entity in self.brick_pieces:
                entity.pos.x -= self.player.vel.x
            for entity in self.fireballs:
                entity.pos.x -= self.player.vel.x
            self.bg_x -= self.player.vel.x / 7
