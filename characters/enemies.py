import pygame as pg

# Local imports
from characters.entity_constants import *
from settings import HEIGHT
from game_setup import IMAGES
from tools import get_image

# Pygame 2D Vector
vec = pg.math.Vector2

class Enemy(pg.sprite.Sprite):
    '''A Base class for enemies'''
    def __init__(self):
        super().__init__()

    def _setup(self, x, y, image, state):
        '''Setup for enemy'''
        self.pos = vec(x, y)
        self.vel = vec(ENEMY_VEL_X, 0)
        self.acc_y = GRAVITY
        self.image = image
        self.mask = pg.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.pos
        self.state = state
        self.kill_timer = 0

    def draw(self,win):
        '''Draws a bounding rectangle around the image'''
        pg.draw.rect(win, (255,0,0), self.rect, 2)

    def spawn(self):
        '''Sets the enemy's state to ACTIVATED'''
        self.state = ACTIVATED

    def _check_collision(self, boxes, pipes, ground_blocks):
        ''''Adjusts enemy for collisions'''     

        # X movement
        self.pos.x += self.vel.x
        self.rect.centerx = self.pos.x
        box = pg.sprite.spritecollideany(self, boxes)
        pipe = pg.sprite.spritecollideany(self, pipes)
        ground = pg.sprite.spritecollideany(self, ground_blocks)

        def adjust_after_x_collision(sprite):
            if self.vel.x > 0:
                self.rect.right = sprite.rect.left
                self.vel.x = -ENEMY_VEL_X
            else:
                self.rect.left = sprite.rect.right
                self.vel.x = ENEMY_VEL_X
            self.pos.x = self.rect.centerx

        if box:
            adjust_after_x_collision(box)
        if pipe:
            adjust_after_x_collision(pipe)
        if ground:
            adjust_after_x_collision(ground)

        # Y movement
        self.pos.y += self.vel.y
        self.rect.bottom = self.pos.y
        box = pg.sprite.spritecollideany(self, boxes)
        pipe = pg.sprite.spritecollideany(self, pipes)
        ground = pg.sprite.spritecollideany(self, ground_blocks)

        def adjust_after_y_collision(sprite):
            if self.vel.y > 0:
                self.rect.bottom = sprite.rect.top
                self.vel.y = 0
            else:
                self.rect.top = sprite.rect.bottom  
            self.pos.y = self.rect.bottom     

        if box:
            adjust_after_y_collision(box)
        if pipe:
            adjust_after_y_collision(pipe)
        if ground:
            adjust_after_y_collision(ground)

    def update(self, current_time, sprite_group):
        '''Updates the enemy's position'''
        self.acc_y = GRAVITY

        if self.vel.y < MAX_VEL_Y:
            # If max speed has not been achieved
            self.vel.y += self.acc_y             

        # Check for collisions
        self.__check_collision(sprite_group)
        self.rect.midbottom = self.pos


class Goomba(Enemy):
    '''A class for a Goomba'''
    def __init__(self, **kwargs):
        super().__init__()
        x = kwargs.get('x')
        y = kwargs.get('y', GROUND - 1)
        state = kwargs.get('state', ACTIVATED)

        self.spritesheet = IMAGES['goomba_sprites']
        self.images = self.__load_images()
        self.image_count = 0
        image = self.images[0]
        self._setup(x, y, image, state)

    def __load_images(self):
        '''Loads images and returns them as a list'''
        width = height = 160

        images = []
        # Right goomba
        images.append(get_image(self.spritesheet, 120, 41, width, height, 0.2))
        # Left goomba
        images.append(get_image(self.spritesheet, 330, 41, width, height, 0.2))
        # Small goomba
        images.append(get_image(self.spritesheet, 540, 121, width, height / 2, 0.2)) 
        # Flipped goomba
        images.append(pg.transform.flip(images[0], False, True))

        return images

    def __animate_jumped_on(self, current_time):
        delta_time = current_time - self.kill_timer
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.pos
        
        if 0 <= delta_time < 800:
            self.image = self.images[2]
        elif delta_time >= 800:
            self.kill()
    
    def __flip(self):
        '''Sets the image the a flipped Goomba'''
        self.image = self.images[3]
    
    def update(self, current_time, boxes, pipes, ground_blocks):
        '''Updates the Goomba'''
        self.acc_y = GRAVITY
        
        # Jumped on
        if self.state == DYING:
            self.acc_y = 0
            self.vel.x = 0
            self.vel.y = 0
            self.__animate_jumped_on(current_time)       
        
        # Shot with fireball or runover with star
        elif self.state == FLIPPED:
            self.__flip()
            self.vel.y += GOOMBA_FALL_GRAVITY
            self.pos += self.vel
            self.rect.midbottom = self.pos

        else:
            if self.vel.y < MAX_VEL_Y:
                # If max speed has not been achieved
                self.vel.y += self.acc_y   

            # Update image and rect
            self.__update_image()
            self.rect = self.image.get_rect()
            self.rect.midbottom = self.pos        

            self._check_collision(boxes, pipes, ground_blocks)
            self.rect.midbottom = self.pos
            self.mask = pg.mask.from_surface(self.image)

        if self.pos.y >= HEIGHT:      
            self.kill()

    def __update_image(self):
        '''Updates the Goomba's image'''
        self.image = self.images[self.image_count // 10 % 2]
        self.image_count += 1


class Turtle(Enemy):
    '''A class for a turtle'''
    def __init__(self, x, y, state=DEACTIVATED):
        super().__init__()
        self._setup(x, y, self.image, state)
