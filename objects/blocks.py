import pygame as pg

# Local imports
from powerups.powerup import Mushroom, FireFlower, Star, Coin
from powerups.powerup_states import *
from characters.entity_constants import *
from tools import get_image, scale_image
from game_setup import IMAGES, SOUND
from settings import HEIGHT

# Pygame 2D Vector
vec = pg.math.Vector2

class QuestionBox(pg.sprite.Sprite):
    '''A class for a question box'''
    def __init__(self, powerup_group, **kwargs):
        super().__init__()
        self.powerups = powerup_group
        x = kwargs.get('x')
        y = kwargs.get('y')
        self.contents = kwargs.get('contents', 'coin')
        self.num_of_pows = kwargs.get('num-of-pows', 1)
        
        self.init_y = y
        self.pos = vec(x, y)
        self.acc = vec(0, 0)
        self.vel = vec(0, 0)

        self.image = pg.transform.scale(get_image(IMAGES['block-sheet'], 0, 0, 24, 24), (42, 42))
        self.opened = pg.transform.scale(IMAGES['block-opened'], (42, 42))
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos

        self.state = CLOSED


    def __spawn_contents(self, player):
        '''Spawns the contents of the question box'''
        self.num_of_pows -= 1       # Decrease number of powerups in the box
        if self.contents == 'coin':
            content = (Coin(self.rect.centerx, self.rect.y))
            player.score += 200     # Coin adds 200 score  
             # add coin to player
            player.coins += 1
             
        
        elif self.contents == 'mushroom':
            content = Mushroom(self.rect.centerx, self.rect.centery, REVEAL, self.rect.y)
        
        elif self.contents == 'fireflower':
            if player.is_large:
                content = FireFlower(self.rect.centerx, self.rect.centery, REVEAL, self.rect.y)
            else:
                content = Mushroom(self.rect.centerx, self.rect.centery, REVEAL, self.rect.y)
        
        elif self.contents == 'star':
            content = Star(self.rect.centerx, self.rect.centery, REVEAL, self.rect.y)
        
        self.powerups.add(content)

    def __move(self):
        '''Updates the position while it is moving vertically'''
        self.acc.y = GRAVITY
        self.vel.y += self.acc.y  

        # Update position
        self.pos += self.vel

        if self.pos.y > self.init_y:
            self.pos.y = self.init_y
            self.state = CLOSED
            self.vel.y = 0

    def update(self, player):
        '''Updates the question box'''
        if self.state != OPENED:
            if self.num_of_pows <= 0 and self.state != MOVING:
                self.state = OPENED
                self.image = self.opened
                self.rect = self.image.get_rect()              
            else:
                if self.state == BUMPED:
                    self.__spawn_contents(player)
                    self.state = MOVING
                    self.vel.y = QBOX_BUMP_VEL
                    self.__move()
                elif self.state == MOVING:
                    self.__move()
        self.rect.topleft = self.pos

class Brick(pg.sprite.Sprite):
    '''A class for a breakable brick'''
    def __init__(self, powerup_group, brick_piece_group, **kwargs):
        super().__init__()
        self.powerups = powerup_group
        self.brick_pieces = brick_piece_group
        x = kwargs.get('x')
        y = kwargs.get('y')
        self.contents = kwargs.get('contents', None)
        self.num_of_pows = kwargs.get('num-of-pows', 1)

        self.pos = vec(x, y)
        self.acc = vec(0, 0)
        self.vel = vec(0, 0)
        self.init_y = y

        self.image = pg.transform.scale(IMAGES['brick_64x64'], (42, 42))
        self.opened = pg.transform.scale(IMAGES['block-opened'], (42, 42))
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos

        # Sounds
        self.break_sound = SOUND['break-brick']
        self.bump_sound = SOUND['bump']

        self.state = CLOSED

    def update(self, player):
        '''Updates the brick'''
        if self.contents:       
            if self.state != OPENED:
                if self.num_of_pows <= 0 and self.state != MOVING:
                    self.state = OPENED
                    self.image = self.opened
                    self.rect = self.image.get_rect()                
                else:
                    if self.state == BUMPED:
                        self.__spawn_contents(player)
                        self.state = MOVING
                        self.vel.y = BRICK_BUMP_VEL
                        self.__move()
        else:
            if self.state == BUMPED:
                if player.is_large:
                    # Destroy brick
                    self.state = BREAKING
                    self.__break()
                    
                else:
                    self.state = MOVING
                    self.vel.y = -5
                    self.bump_sound.play()
                    self.__move()
        
        if self.state == MOVING:
            self.__move()

        elif self.state == BREAKING:
            self.__break()

        self.rect.topleft = self.pos

    def __break(self):
        '''Spawns brick pieces and kills itself'''
        x = self.rect.centerx
        y = self.rect.centery
        positions = [TOP_LEFT, TOP_RIGHT, BOTTOM_LEFT, BOTTOM_RIGHT]
        for pos in positions:
            self.brick_pieces.add(BrickPiece(x, y, pos))

        self.break_sound.play()
        self.kill()

    def __move(self):
        '''Moves the brick vertically'''
        self.acc.y = GRAVITY
        self.vel.y += self.acc.y  

        # Update position
        self.pos += self.vel

        if self.pos.y > self.init_y:
            self.pos.y = self.init_y
            self.state = CLOSED
            self.vel.y = 0

    def __spawn_contents(self, player):
        '''Spawns contents from the brick'''
        self.num_of_pows -= 1       # Decrease number of powerups in the box
        if self.contents == 'coin':
            coin = (Coin(self.rect.centerx, self.rect.y))
            self.powerups.add(coin)
            player.score += 200     # Coin adds 200 score           


class BrickPiece(pg.sprite.Sprite):
    '''A class for the pieces that appear when a brick is destroyed'''
    def __init__(self, x, y, location):
        super().__init__()
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.acc = vec(0, BRICK_PIECE_GRAVITY)
        self.corner = location    # TOP_LEFT, TOP_RIGHT, BOTTOM_LEFT or BOTTOM_RIGHT
        self.image = self.__get_image()
        self.orig_image = self.image # Copy of image
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.__setup_pos_and_vel((x, y), location)
        self.location = location
        self.angle = 0          # Starting rotation value in degrees

    def __get_image(self):
        '''Returns the correct image based on self.corner'''
        img_dict = {
            TOP_LEFT: IMAGES['brick-small'],
            TOP_RIGHT: IMAGES['brick-corner'],
            BOTTOM_RIGHT: IMAGES['brick-big'],
            BOTTOM_LEFT: IMAGES['brick-corner']
        }   
        
        return scale_image(img_dict[self.corner], BRICK_PIECE_SCALAR)

    def __setup_pos_and_vel(self, pos, location):
        '''Sets up appropriate pos and vel values'''
        if location == TOP_LEFT:
            self.rect.bottomright = pos
            self.vel.x = -LOW_BRICK_PIECE_VEL_X
            self.vel.y = HIGH_BRICK_PIECE_VEL_Y
        
        elif location == TOP_RIGHT:
            self.rect.bottomleft = pos
            self.vel.x = LOW_BRICK_PIECE_VEL_X
            self.vel.y = LOW_BRICK_PIECE_VEL_Y
        
        elif location == BOTTOM_LEFT:
            self.rect.topright = pos
            self.vel.x = -HIGH_BRICK_PIECE_VEL_X
            self.vel.y = MED_BRICK_PIECE_VEL_Y
        
        elif location == BOTTOM_RIGHT:
            self.rect.topleft = pos
            self.vel.x = HIGH_BRICK_PIECE_VEL_X
            self.vel.y = MED_BRICK_PIECE_VEL_Y

    def update(self):
        '''Updates the brick piece'''
        self.vel += self.acc
        self.pos += self.vel
        
        self.__adjust_rect()
        
        self.__rotate()
        self.angle += 2

        if self.rect.top > HEIGHT:
            self.kill()

    def __adjust_rect(self):
        if self.location == TOP_LEFT:
            self.rect.bottomright = self.pos
        elif self.location == TOP_RIGHT:
            self.rect.bottomleft = self.pos
        elif self.location == BOTTOM_LEFT:
            self.rect.topright = self.pos   
        elif self.location == BOTTOM_RIGHT:
            self.rect.topleft = self.pos    

    def __rotate(self):
        '''Rotates the image around its origin'''      
        self.image = pg.transform.rotozoom(self.orig_image, self.angle, 1)
        self.rect = self.image.get_rect(center=self.rect.center)
