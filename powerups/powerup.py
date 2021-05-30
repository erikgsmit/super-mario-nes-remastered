import pygame as pg

# Local imports
from labels import ScoreLabel
from settings import *
from characters import entity_constants as ec
from powerups.powerup_states import *
from game_setup import IMAGES, SOUND
from tools import get_image


# Pygame 2D Vector
vec = pg.math.Vector2


class Powerup(pg.sprite.Sprite):
    '''A base class for powerups'''
    def __init__(self):
        super().__init__()
    
    def _setup(self, x, y, img, initial_state, box_y):
        '''Setup for powerups'''
        self.pos = vec(x, y)
        self.vel = vec(ec.MUSHROOM_VEL_X, 0)
        self.acc = vec(0, ec.GRAVITY)
        self.box_y = box_y
        self.image = img
        self.rect = self.image.get_rect() 
        self.rect.midbottom = self.pos 
        self.mask = pg.mask.from_surface(self.image)
        self.state = initial_state

    def _check_collision(self, boxes, ground_blocks, pipes):
        '''Checks for collisions with boxes, ground blocks and pipes'''

        # X movement
        self.pos.x += self.vel.x
        self.rect.centerx = self.pos.x
        box = pg.sprite.spritecollideany(self, boxes)
        ground = pg.sprite.spritecollideany(self, ground_blocks)
        pipe = pg.sprite.spritecollideany(self, pipes)

        def adjust_after_x_collision(sprite):
            if self.vel.x > 0:
                self.rect.right = sprite.rect.left
            else:
                self.rect.left = sprite.rect.right
            self.vel.x *= -1
            self.pos.x = self.rect.centerx

        if box:
            adjust_after_x_collision(box)
        if ground:
            adjust_after_x_collision(ground)
        if pipe: 
            adjust_after_x_collision(pipe)

        # Y movement
        self.pos.y += self.vel.y
        self.rect.bottom = self.pos.y
        box = pg.sprite.spritecollideany(self, boxes)
        ground = pg.sprite.spritecollideany(self, ground_blocks)
        pipe = pg.sprite.spritecollideany(self, pipes)

        def adjust_after_y_collision(sprite):
            if self.vel.y > 0:
                self.rect.bottom = sprite.rect.top
                self.vel.y = 0
            else:
                self.rect.top = sprite.rect.bottom
            self.pos.y = self.rect.bottom

        if box:
            adjust_after_y_collision(box)
        if ground:
            adjust_after_y_collision(ground)
        if pipe:
            adjust_after_y_collision(pipe)
    
    def _reveal(self):
        '''Moves the powerup up through the box'''
        self.vel.x = 0
        self.vel.y = -1
        self.pos.y += self.vel.y
        
        if self.rect.bottom <= self.box_y:
            # Powerup has gone through entire box
            self.pos.y = self.box_y
            self.state = ACTIVATED
        
        self.rect.midbottom = self.pos


class Mushroom(Powerup):
    '''A class for a mushroom powerup'''
    def __init__(self, x, y, initial_state=REVEAL, box_y=0):
        super().__init__()
        img = pg.transform.scale(IMAGES['mario_redshroom'], (27, 27))
        self._setup(x, y, img, initial_state, box_y)

    def update(self, labels, *groups):
        '''Updates the position of the powerup'''        
        if self.state == ACTIVATED:
            self.acc.y = ec.GRAVITY

            if self.vel.x == 0:
                self.vel.x = ec.MUSHROOM_VEL_X

            if self.vel.y < ec.MAX_VEL_Y:
                # If max speed has not been achieved
                self.vel.y += self.acc.y

            # Check for collisions
            self._check_collision(*groups)
            self.rect.midbottom = self.pos
            self.mask = pg.mask.from_surface(self.image)

        elif self.state == REVEAL:
            self._reveal()


class FireFlower(Powerup):
    '''A class for a fire flower powerup'''
    def __init__(self, x, y, initial_state=REVEAL, box_y=0):
        super().__init__()
        img = pg.transform.scale(IMAGES['fireflower'], (27, 27))
        self._setup(x, y, img, initial_state, box_y)
  
    def update(self, labels, *args):
        '''Updates the fire flower'''
        if self.state == REVEAL:
            self._reveal()
            # Update position 
            self.pos += self.vel
        self.rect.midbottom = self.pos
        self.mask = pg.mask.from_surface(self.image)


class Fireball(pg.sprite.Sprite):
    '''A class for the fireballs mario can shoot'''
    def __init__(self, x, y, direction):
        super().__init__()
        self.pos = vec(x, y)
        self.vel = vec(ec.FIREBALL_VEL_X, 0)
        self.acc = vec(0, ec.GRAVITY)

        self.image = self.__get_image(direction)
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.pos 

        self.hit_sound = SOUND['fireball-hit']
        self.hit_enemy_sound = SOUND['kick']
        self.hit_enemy_sound.set_volume(.5)

    def __get_image(self, direction):
        '''Returns the correct image based on orientation'''
        img = IMAGES['fireball-2']
        img = pg.transform.scale(
            img,
            (
                round(0.02 * img.get_width()),
                round(0.02 * img.get_height())
            )
        )

        if direction == ec.LEFT:
            self.vel.x *= -1
            # Flips the image horizontally
            img = pg.transform.flip(img, True, False)
        
        return img

    def update(self,player,labels, boxes, ground, pipes, enemies):
        '''Updates the fireball'''
        self.acc = vec(0, ec.GRAVITY)

        # Update y speed
        if self.vel.y < ec.MAX_VEL_Y:
            # If max speed has not been achieved
            self.vel.y += self.acc.y 

        self.__collision(player,labels,boxes, ground, pipes, enemies)
        self.rect.midbottom = self.pos

    def __collision(self, player, labels, boxes, ground_blocks, pipes, enemies):
        '''Check fireball collision'''       
        
        # X movement
        self.pos.x += self.vel.x
        self.rect.centerx = self.pos.x
        box = pg.sprite.spritecollideany(self, boxes)
        ground = pg.sprite.spritecollideany(self, ground_blocks)
        pipe = pg.sprite.spritecollideany(self, pipes)
    
        def adjust_after_x_solid_collision(sprite):
            if self.vel.x > 0:
                self.rect.right = sprite.rect.left
            else:
                self.rect.left = sprite.rect.right
            self.hit_sound.play()
            self.pos.x = self.rect.centerx
            self.kill()

        if box:
            adjust_after_x_solid_collision(box)
        if ground:
            adjust_after_x_solid_collision(ground)
        if pipe:
            adjust_after_x_solid_collision(pipe)

        # Y movement
        self.pos.y += self.vel.y
        self.rect.bottom = self.pos.y
        enemy = pg.sprite.spritecollideany(self, enemies)
        box = pg.sprite.spritecollideany(self, boxes)
        ground = pg.sprite.spritecollideany(self, ground_blocks)
        pipe = pg.sprite.spritecollideany(self, pipes)
        
        if enemy and enemy.state != ec.FLIPPED and enemy.state != ec.DYING:
            enemy.state = ec.FLIPPED
            enemy.vel.y = -11
            enemy.vel.x = 0.3 * self.vel.x
            self.hit_enemy_sound.play()
            # Create score label
            score_label = ScoreLabel('1000', enemy.rect.centerx, enemy.rect.centery)
            labels.append(score_label)
            player.score += 1000
            self.kill()
    
        def adjust_after_y_solid_collision(sprite):
            if self.vel.y > 0:
                self.rect.bottom = sprite.rect.top
                self.vel.y = ec.FIREBALL_BOUNCE_VEL_Y
            else:
                self.rect.top = sprite.rect.bottom
                self.hit_sound.play()
                self.kill()
            self.pos.y = self.rect.bottom

        if box:
            adjust_after_y_solid_collision(box)
        if ground:
            adjust_after_y_solid_collision(ground)
        if pipe:
            adjust_after_y_solid_collision(pipe)
    
class Star(Powerup):
    '''A class for a star powerup'''
    def __init__(self, x, y, initial_state=REVEAL, box_y=0):
        super().__init__()
        img = pg.transform.scale(IMAGES['star'], (32, 32))
        self._setup(x, y, img, initial_state, box_y)
        self.direction = ec.RIGHT
        self.acc = vec(0, ec.STAR_GRAVITY)
    
    def update(self, labels, *groups):
        '''Updates the star'''
        if self.state == REVEAL:
            self._reveal()
            self.vel.x = ec.STAR_VEL_X

        elif self.state == ACTIVATED:            
            if self.vel.y < ec.STAR_VEL_Y:
            # If max speed has not been achieved
                self.vel.y += self.acc.y 

            self.__check_collision(*groups)
            self.mask = pg.mask.from_surface(self.image)

    def __check_collision(self, boxes, ground_blocks, pipes):
        '''Checks for collisions with obstacles''' 

        # X movement
        self.pos.x += self.vel.x
        self.rect.centerx = self.pos.x
        box = pg.sprite.spritecollideany(self, boxes)
        ground = pg.sprite.spritecollideany(self, ground_blocks)
        pipe = pg.sprite.spritecollideany(self, pipes)

        def adjust_after_x_collision(sprite):
            if self.vel.x > 0:
                self.rect.right = sprite.rect.left
            else:
                self.rect.left = sprite.rect.right
            self.vel.x *= -1
            self.pos.x = self.rect.centerx

        if box:
            adjust_after_x_collision(box)
        if ground:
            adjust_after_x_collision(ground)
        if pipe:
            adjust_after_x_collision(pipe)

        # Y movement
        self.pos.y += self.vel.y
        self.rect.bottom = self.pos.y
        box = pg.sprite.spritecollideany(self, boxes)
        ground = pg.sprite.spritecollideany(self, ground_blocks)
        pipe = pg.sprite.spritecollideany(self, pipes)

        def adjust_after_y_collision(sprite):
            if self.vel.y > 0:
                self.rect.bottom = sprite.rect.top
                self.vel.y = -ec.STAR_VEL_Y
            else:
                self.rect.top = sprite.rect.bottom
                self.vel.y = ec.STAR_VEL_Y
            self.pos.y = self.rect.bottom

        if box:
            adjust_after_y_collision(box)
        if ground:
            adjust_after_y_collision(ground)
        if pipe:
            adjust_after_y_collision(pipe)


class Coin(Powerup):
    '''A class for a coin'''
    def __init__(self, x, y):
        super().__init__()
        self.spritesheet = IMAGES['coin_sheet']
        img = get_image(self.spritesheet, 147, 150, 62, 61)
        self._setup(x, y, img, REVEAL, y)

        self.images = self.__load_images()
        self.acc = vec(0, ec.GRAVITY)
        self.vel.y = ec.COIN_VEL_Y
        self.count = 0

        # Sounds
        self.coin_sound = SOUND['coin']
        self.coin_sound.set_volume(0.1)
        self.coin_sound.play()

    def __load_images(self):
        '''Loads images and returns them as a list'''
        start_x = 147
        start_y = 150
        width = 62
        height = 61

        images = []
        # Appends all necessary images from the sprite sheet to the images list
        for i in range(6):
            x = start_x + i*(width)
            y = start_y
            images.append(pg.transform.scale(
                get_image(self.spritesheet, x, y, width, height), 
                (round(0.4 * width), round(0.4 * height)))
            )

        return images

    def update(self, labels, *args):
        '''Updates the position of the coin'''
        self.vel.x = 0
        self.vel.y += self.acc.y
        self.pos += self.vel
        if self.pos.y >= self.box_y:
            # Spawn score label
            score_label = ScoreLabel('200', self.rect.x, self.rect.y)
            labels.append(score_label)
            self.kill()
        self.__update_image()

    def __update_image(self):
        '''Animates between images'''
        self.image = self.images[(self.count // 2) % len(self.images)]
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.pos
        self.count += 1
