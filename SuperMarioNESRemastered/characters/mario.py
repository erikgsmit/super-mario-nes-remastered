import json
import pygame as pg

# Local imports
from objects.blocks import QuestionBox, Brick
from powerups.powerup import Mushroom, FireFlower, Fireball, Star
from game_setup import IMAGES, DATA, SOUND, MUSIC
from powerups.powerup_states import *
from settings import *
from characters.entity_constants import *
from characters.enemies import Goomba
from tools import get_image
import labels as lbl

# Pygame 2D vector
vec = pg.math.Vector2


class Player(pg.sprite.Sprite):
    '''A class for the main player in the game'''    
    def __init__(self):
        super().__init__()
        self.__load_images_from_file(IMAGES['mario'])
        self.image = self.normal_small_frames[0][0]
        self.rect = self.image.get_rect()
        self.mask = pg.mask.from_surface(self.image)

        # Score
        self.score = 0
        self.coins = 0
        self.lives = STARTING_LIVES

        self.pow = NO_POW
        self.fireballs = pg.sprite.Group()

        # Timer for shooting fireballs and grow large
        self.fireball_shot = 0
        self.invincible_index = 0
        
        self.__setup_booleans()
        self.__setup_timers()
        self.__setup_motions()

        self.image_index = 0
        self.state = RESTING
        # Sounds
        self.__load_sounds()

    def __setup_motions(self):
        self.pos = vec(MARIO_START_X, GROUND)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.gravity = GRAVITY
        self.dir = RIGHT
        self.rect.midbottom = self.pos

    def __setup_booleans(self):
        '''Sets up booleans'''
        self.is_transition = False
        self.is_large = False
        self.has_star = False
        self.losing_invincibility = False
        self.is_jumping = False
        self.is_falling = False
        self.allow_jump = True
        self.is_walking = False
        self.is_invincible = False
        self.song_is_playing = False

    def __setup_timers(self):
        '''Sets up timers'''
        self.current_timer = pg.time.get_ticks()
        self.transition_timer = 0
        self.walk_timer = 0
        self.invincible_begin_timer = 0
        self.star_timer = 0

    def __load_sounds(self):
        '''Loads in all sounds for mario'''
        self.shrink_sound = SOUND['get_small']
        self.jump_small_sound = SOUND['jump-mini-wii']
        self.jump_small_sound.set_volume(.5)
        self.jump_large_sound = SOUND['jump-wii']
        self.jump_large_sound.set_volume(.5)
        self.fire_sound = SOUND['fireball-wii']
        self.fire_sound.set_volume(.5)
        self.grow_large_sound = SOUND['grow-large']
        self.hit_enemy_sound = SOUND['kick']
        self.hit_enemy_sound.set_volume(.5)

    def __load_images(self, spritesheet):
        '''Loads all images for mario'''

        # Images for normal small mario
        right_small_normal_frames = [
            get_image(spritesheet, 178, 32, 12, 16),  # Right [0]
            get_image(spritesheet,  80, 32, 15, 16),  # Right walking 1 [1]
            get_image(spritesheet,  96, 32, 16, 16),  # Right walking 2 [2]
            get_image(spritesheet, 112, 32, 16, 16),  # Right walking 3 [3]
            get_image(spritesheet, 144, 32, 16, 16),  # Right jump [4]
            pg.transform.flip(get_image(spritesheet, 130, 32, 14, 16), True, False),  # Right skid [5]
            get_image(spritesheet, 160, 32, 15, 16),  # Death frame [6]
            get_image(spritesheet, 320,  8, 16, 24),  # Transition small to big [7]
            get_image(spritesheet, 241, 33, 16, 16),  # Transition big to small [8]
            get_image(spritesheet, 194, 32, 12, 16),  # Frame 1 of flag pole Slide [9]
            get_image(spritesheet, 210, 33, 12, 16)   # Frame 2 of flag pole slide [10]
        ]

        # Images for small green mario (for invincible animation)
        right_small_green_frames = [
            get_image(spritesheet, 178, 224, 12, 16),  # Right standing [0]
            get_image(spritesheet,  80, 224, 15, 16),  # Right walking 1 [1]
            get_image(spritesheet,  96, 224, 16, 16),  # Right walking 2 [2]
            get_image(spritesheet, 112, 224, 15, 16),  # Right walking 3 [3]
            get_image(spritesheet, 144, 224, 16, 16),  # Right jump [4]
            pg.transform.flip(get_image(spritesheet, 130, 224, 14, 16), True, False)  # Right skid [5]
        ]

        # Images for small red mario (for invincible animation)
        right_small_red_frames = [
            get_image(spritesheet, 178, 272, 12, 16),  # Right standing [0]
            get_image(spritesheet,  80, 272, 15, 16),  # Right walking 1 [1]
            get_image(spritesheet,  96, 272, 16, 16),  # Right walking 2 [2]
            get_image(spritesheet, 112, 272, 15, 16),  # Right walking 3 [3]
            get_image(spritesheet, 144, 272, 16, 16),  # Right jump [4]
            pg.transform.flip(get_image(spritesheet, 130, 272, 14, 16), True, False)  # Right skid [5]
        ]

        # Images for small black mario (for invincible animation)
        right_small_black_frames = [
            get_image(spritesheet, 178, 176, 12, 16),  # Right standing [0]
            get_image(spritesheet,  80, 176, 15, 16),  # Right walking 1 [1]
            get_image(spritesheet,  96, 176, 16, 16),  # Right walking 2 [2]
            get_image(spritesheet, 112, 176, 15, 16),  # Right walking 3 [3]
            get_image(spritesheet, 144, 176, 16, 16),  # Right jump [4]
            pg.transform.flip(get_image(spritesheet, 130, 176, 14, 16), True, False)  # Right skid [5]
        ]

        # Images for normal big Mario
        right_big_normal_frames = [
            get_image(spritesheet, 176,  0, 16, 32),  # Right standing [0]
            get_image(spritesheet,  81,  0, 16, 32),  # Right walking 1 [1]
            get_image(spritesheet,  97,  0, 15, 32),  # Right walking 2 [2]
            get_image(spritesheet, 113,  0, 15, 32),  # Right walking 3 [3]
            get_image(spritesheet, 144,  0, 16, 32),  # Right jump [4]
            pg.transform.flip(get_image(spritesheet, 128, 0, 16, 32), True, False),  # Right skid [5]
            get_image(spritesheet, 336,  0, 16, 32),  # Right throwing [6]
            get_image(spritesheet, 160, 10, 16, 22),  # Right crouching [7]
            get_image(spritesheet, 272,  2, 16, 29),  # Transition big to small [8]
            get_image(spritesheet, 193,  2, 16, 30),  # Frame 1 of flag pole slide [9]
            get_image(spritesheet, 209,  2, 16, 29)   # Frame 2 of flag pole slide [10]
        ]

        # Images for green big Mario
        right_big_green_frames = [
            get_image(spritesheet, 176, 192, 16, 32),  # Right standing [0]
            get_image(spritesheet,  81, 192, 16, 32),  # Right walking 1 [1]
            get_image(spritesheet,  97, 192, 15, 32),  # Right walking 2 [2]
            get_image(spritesheet, 113, 192, 15, 32),  # Right walking 3 [3]
            get_image(spritesheet, 144, 192, 16, 32),  # Right jump [4]
            pg.transform.flip(get_image(spritesheet, 128, 192, 16, 32), True, False),  # Right skid [5]
            get_image(spritesheet, 336, 192, 16, 32),  # Right throwing [6]
            get_image(spritesheet, 160, 202, 16, 22)   # Right Crouching [7]
        ]

        # Images for red big Mario
        right_big_red_frames = [
            get_image(spritesheet, 176, 240, 16, 32),  # Right standing [0]
            get_image(spritesheet,  81, 240, 16, 32),  # Right walking 1 [1]
            get_image(spritesheet,  97, 240, 15, 32),  # Right walking 2 [2]
            get_image(spritesheet, 113, 240, 15, 32),  # Right walking 3 [3]
            get_image(spritesheet, 144, 240, 16, 32),  # Right jump [4]
            pg.transform.flip(get_image(spritesheet, 128, 240, 16, 32), True, False),  # Right skid [5]
            get_image(spritesheet, 336, 240, 16, 32),  # Right throwing [6]
            get_image(spritesheet, 160, 250, 16, 22)   # Right crouching [7]
        ]

        # Images for black big Mario
        right_big_black_frames = [
            get_image(spritesheet, 176, 144, 16, 32),  # Right standing [0]
            get_image(spritesheet,  81, 144, 16, 32),  # Right walking 1 [1]
            get_image(spritesheet,  97, 144, 15, 32),  # Right walking 2 [2]
            get_image(spritesheet, 113, 144, 15, 32),  # Right walking 3 [3]
            get_image(spritesheet, 144, 144, 16, 32),  # Right jump [4]
            pg.transform.flip(get_image(spritesheet, 128, 144, 16, 32), True, False),  # Right skid [5]
            get_image(spritesheet, 336, 144, 16, 32),  # Right throwing [6]
            get_image(spritesheet, 160, 154, 16, 22)   # Right Crouching [7]
        ]

        # Images for Fire Mario
        right_fire_frames = [
            get_image(spritesheet, 176, 48, 16, 32),  # Right standing [0]
            get_image(spritesheet,  81, 48, 16, 32),  # Right walking 1 [1]
            get_image(spritesheet,  97, 48, 15, 32),  # Right walking 2 [2]
            get_image(spritesheet, 113, 48, 15, 32),  # Right walking 3 [3]
            get_image(spritesheet, 144, 48, 16, 32),  # Right jump [4]
            pg.transform.flip(get_image(spritesheet, 128, 48, 16, 32), True, False),  # Right skid [5]
            get_image(spritesheet, 336, 48, 16, 32),  # Right throwing [6]
            get_image(spritesheet, 160, 58, 16, 22),  # Right crouching [7]
            get_image(spritesheet,   0,  0,  0,  0),  # Place holder [8]
            get_image(spritesheet, 193, 50, 16, 29),  # Frame 1 of flag pole slide [9]
            get_image(spritesheet, 209, 50, 16, 29)   # Frame 2 of flag pole slide [10]
        ]
        
        def right_and_flipped(img_list):
            '''Returns a 2D list with the image list and a flipped image list'''            
            def flip_image_list(list_to_flip):
                '''Returns a list of each image flipped horizontally'''
                return [pg.transform.flip(frame, True, False) for frame in list_to_flip]
        
            return [img_list, flip_image_list(img_list)]

        # Makes 2 dimensional lists of the right and left frames
        self.normal_small_frames = right_and_flipped(right_small_normal_frames)
        self.green_small_frames  = right_and_flipped(right_small_green_frames)
        self.red_small_frames    = right_and_flipped(right_small_red_frames)
        self.black_small_frames  = right_and_flipped(right_small_black_frames)
        self.normal_big_frames   = right_and_flipped(right_big_normal_frames)
        self.green_big_frames    = right_and_flipped(right_big_green_frames)
        self.red_big_frames      = right_and_flipped(right_big_red_frames)
        self.black_big_frames    = right_and_flipped(right_big_black_frames)
        self.fire_frames         = right_and_flipped(right_fire_frames)

        # Invincible Mario lists
        self.invincible_small_frames_list = [
            self.normal_small_frames,
            self.green_small_frames,
            self.red_small_frames,
            self.black_small_frames
        ]
        self.invincible_big_frames_list = [
            self.normal_big_frames,
            self.green_big_frames,
            self.red_big_frames,
            self.black_big_frames
        ]

    def __load_images_from_file(self, spritesheet):
        '''Uses json data to load all images'''
        with open(DATA['mario']) as f:
            data = json.load(f)
        
        def flip_image_list(list_to_flip):
            '''Returns a list of each image flipped horizontally'''
            return [pg.transform.flip(frame, True, False) for frame in list_to_flip]
    
        def get_frames(type):
            img_list = [get_image(spritesheet, *img, PLAYER_SCALAR) for img in data[type]]
            img_list[5] = pg.transform.flip(img_list[5], True, False)
        
            return [img_list, flip_image_list(img_list)]

        self.normal_small_frames = get_frames('small-normal')
        self.green_small_frames  = get_frames('small-green')
        self.red_small_frames    = get_frames('small-red')
        self.black_small_frames  = get_frames('small-black')
        self.normal_big_frames   = get_frames('big-normal')
        self.green_big_frames    = get_frames('big-green')
        self.red_big_frames      = get_frames('big-red')
        self.black_big_frames    = get_frames('big-black')
        self.fire_frames         = get_frames('fire')
        
        # Invincible Mario lists
        self.invincible_small_frames_list = [
            self.normal_small_frames,
            self.green_small_frames,
            self.red_small_frames,
            self.black_small_frames
        ]
        self.invincible_big_frames_list = [
            self.normal_big_frames,
            self.green_big_frames,
            self.red_big_frames,
            self.black_big_frames
        ]

    def draw(self, win):
        '''Draws a bounding rectangle around the image'''
        pg.draw.rect(win, (255, 0, 0), self.rect, 1)

    def update(self, current_time, keys, labels, flagpole, *groups):
        '''Updates the player'''
        if not self.is_transition:
            if self.state == JUMPING:
                self.__jumping(keys)

            self.acc = vec(0, self.gravity)
            self.is_jumping = self.vel.y != 0 

            self.__check_actions(keys, current_time)
            self.__set_acc_and_vel() 
            self.__update_image_index()
            self.__handle_images(current_time)

            if self.image_index + 1 >= 27:
                self.image_index = 0

            # Sets the rect to the selected image
            self.rect = self.image.get_rect()
            # Sets the midbottom of the image rectangle to the player position
            self.rect.midbottom = self.pos
            self.mask = pg.mask.from_surface(self.image)

            # Check for collisions
            self.__move_and_collide(labels, flagpole, *groups)

            # Check that mario doesnt fall off the map
            if self.rect.top >= HEIGHT:
                self.lives -= 1

        else: 
            self.is_invincible = True
            self.vel.x = 0

            if self.state == GROWING_LARGE:
                # Player will not be able to move while animating
                self.__grow_large(current_time)
            elif self.state == LARGE_TO_SMALL:
                self.__large_to_small(current_time)
            elif self.state == LARGE_TO_FIRE:
                self.__large_to_fire(current_time)
            elif self.state == FIRE_TO_LARGE:
                self.__fire_to_large(current_time)
            elif self.state == POLE_SLIDING:
                self.__pole_slide(current_time, flagpole)
            
            self.rect = self.image.get_rect()

        self.__check_invincible_timer()
        self.rect.midbottom = self.pos
        self.current_timer = pg.time.get_ticks()

    def __check_invincible_timer(self):
        if not self.has_star and self.current_timer - self.invincible_begin_timer >= 2000:
            self.is_invincible = False

    def reset(self):
        self.pos.x = MARIO_START_X
        self.pos.y = GROUND - 20
        self.rect.midbottom = self.pos
        self.is_large = False
        self.pow = NO_POW
        self.state = RESTING
        self.has_star = False

    def __jump(self): 
        '''Makes the player jump'''   
        self.state = JUMPING
        self.gravity = JUMP_GRAVITY
        self.vel.y = STAR_JUMP_VEL if self.has_star else JUMP_VEL
       
    def __middle_image(self):
        '''Used for transition from small to big mario'''
        self.image = self.normal_small_frames[self.dir][7]
        
    def __small_image(self):
        '''Used for transition from small to big mario'''
        self.image = self.normal_small_frames[self.dir][0]

    def __large_image(self):
        '''Used for transition from small to big mario'''
        self.image = self.normal_big_frames[self.dir][0]   

    def __red_image(self):
        return self.red_big_frames[self.dir][self.image_index]
     
    def __black_image(self):
        return self.black_big_frames[self.dir][self.image_index]
    
    def __green_image(self):
        return self.green_big_frames[self.dir][self.image_index]

    def __fire_image(self):
        return self.fire_frames[self.dir][self.image_index]
    
    def __normal_image(self):
        return self.normal_big_frames[self.dir][self.image_index]

    def __pole_slide(self, current_time, flagpole):
        self.vel.x = 0
        self.vel.y = SLIDING_VEL
        self.dir = RIGHT

        block = pg.sprite.Group(flagpole.sprites()[3])

        def image(index):
            self.image_index = index
            if self.is_large and self.pow == NO_POW and not self.has_star:
                self.image = self.normal_big_frames[self.dir][self.image_index]
            elif self.pow == FIRE and not self.has_star:
                self.image = self.fire_frames[self.dir][self.image_index]
            elif self.has_star:
                if current_time - self.invincible_begin_timer < 10000:
                    self.__star_animation(current_time, 30)
                elif current_time - self.invincible_begin_timer < 12000:
                    self.__star_animation(current_time, 100)
            else:
                self.image = self.normal_small_frames[self.dir][self.image_index]

        collide_block = pg.sprite.spritecollideany(self, block)

        if collide_block:
            print('YES')
            self.state = END
            self.rect.bottom = collide_block.rect.top
            self.pos.x = self.rect.centerx
            self.pos.y = self.rect.bottom
            self.vel.x = 0
            self.vel.y = 0
        else:
            delta_time = current_time - self.transition_timer

            if 0 <= delta_time < 100:
                image(9)
            elif 100 <= delta_time < 200:
                image(10)
            elif 200 <= delta_time < 300:
                image(9)
            elif 300 <= delta_time < 400:
                image(10)
            elif 400 <= delta_time < 500:
                image(9)
            elif 500 <= delta_time < 600:
                image(10)
            elif 600 <= delta_time < 700:
                image(9)
            elif 700 <= delta_time < 800:
                image(10)

            self.pos += self.vel


    def __grow_large(self, current_time):
        '''Animates mario during a GROWING_LARGE state'''
        self.invincible_begin_timer = current_time         
        delta_time = current_time - self.transition_timer
        
        if 0 <= delta_time < 100:
            self.__small_image()
        elif 100 <= delta_time < 200:
            self.__middle_image()
        elif 200 <= delta_time < 300:
            self.__small_image()
        elif 300 <= delta_time < 400:
            self.__middle_image()
        elif 400 <= delta_time < 500:
            self.__small_image()
        elif 500 <= delta_time < 600:
            self.__middle_image()
        elif 600 <= delta_time < 700:
            self.__small_image()
        elif 700 <= delta_time < 800:
            self.__middle_image()
        elif delta_time >= 800:
            self.__large_image()
            self.state = RESTING
            self.is_transition = False
            self.is_large = True
        else:
            self.state = RESTING
            self.is_large = True

    def __large_to_fire(self, current_time):
        self.invincible_begin_timer = current_time  
        delta_time = current_time - self.transition_timer
        
        if 0 <= delta_time < 100:
            self.image = self.__normal_image()
        elif 100 <= delta_time < 200:
            self.image = self.__fire_image()
        elif 200 <= delta_time < 300:
            self.image = self.__green_image()
        elif 300 <= delta_time < 400:
            self.image = self.__red_image()
        elif 400 <= delta_time < 500:
            self.image = self.__black_image()
        elif 500 <= delta_time < 600:
            self.image = self.__fire_image()
        elif 600 <= delta_time < 700:
            self.image = self.__green_image()
        elif 700 <= delta_time < 800:
            self.image = self.__red_image()
        elif 800 <= delta_time < 900:
            self.image = self.__black_image()     
        elif 900 <= delta_time < 1000:
            self.image = self.__fire_image()
        elif 1000 <= delta_time < 1100:
            self.image = self.__green_image()
        elif 1100 <= delta_time < 1200:
            self.image = self.__red_image()
        elif 1200 <= delta_time:
            self.image = self.__fire_image()
            self.state = RESTING
            self.is_transition = False
        else:
            self.state == RESTING
            self.is_large = False

    def __large_to_small(self, current_time):
        '''Animates mario during a LARGE_TO_SMALL state''' 
        self.invincible_begin_timer = current_time     
        delta_time = current_time - self.transition_timer
        
        if 0 <= delta_time < 100:
            self.__large_image()
        elif 100 <= delta_time < 200:
            self.__middle_image()
        elif 200<= delta_time < 300:
            self.__large_image()
        elif 300 <= delta_time < 400:
            self.__middle_image()
        elif 400 <= delta_time < 500:
            self.__large_image()
        elif 500 <= delta_time < 600:
            self.__middle_image()
        elif 600 <= delta_time < 700:
            self.__large_image()
        elif 700 <= delta_time < 800:
            self.__middle_image()
        elif delta_time >= 800:
            self.__small_image()
            self.state = RESTING
            self.is_transition = False
            self.is_large = False
        else:
            self.state == RESTING
            self.is_large = False
    
    def __fire_to_large(self, current_time):
        '''Animates mario during a LARGE_TO_FIRE state'''
        self.invincible_begin_timer = current_time  
        delta_time = current_time - self.transition_timer
        
        if 0 <= delta_time < 100:
            self.image = self.__fire_image()
        elif 100 <= delta_time < 200:
            self.image = self.__normal_image()
        elif 200 <= delta_time < 300:
            self.image = self.__fire_image()
        elif 300 <= delta_time < 400:
            self.image = self.__normal_image()
        elif 400 <= delta_time < 500:
            self.image = self.__fire_image()
        elif 500 <= delta_time < 600:
            self.image = self.__normal_image()
        elif 600 <= delta_time < 700:
            self.image = self.__fire_image()
        elif 700 <= delta_time:
            self.image = self.__normal_image()
            self.state = RESTING
            self.is_transition = False
            self.pow = NO_POW
    
    def __star_animation(self, current_time, interval):
        '''Animates mario when in possesion of a star'''
        if current_time - self.star_timer >= interval:
            if self.invincible_index < len(self.invincible_small_frames_list) - 1:
                self.invincible_index += 1
            else:
                self.invincible_index = 0

            if self.is_large:
                # pickout the large mario frames of the right color
                frames = self.invincible_big_frames_list[self.invincible_index]
            else:
                frames = self.invincible_small_frames_list[self.invincible_index]
                # pickout the large mario frames of the right color

            self.star_timer = current_time
            self.image = frames[self.dir][self.image_index]

    def __move_and_collide(self, labels, flagpole, powerups, boxes, pipes, ground_blocks, enemies):
        '''Updates Mario's position and handles collisions'''

        def coll_group(*groups):
            return (pg.sprite.spritecollideany(self, group) for group in groups)

        # X movement
        self.pos.x += self.vel.x
        if self.pos.x < 20:
            self.pos.x = 20
        self.rect.centerx = self.pos.x

        collisions = coll_group(boxes, pipes, ground_blocks, flagpole, enemies)
        self.__adjust_after_x_collisions(labels, *collisions)

        # Y movement
        self.pos.y += self.vel.y
        self.rect.bottom = self.pos.y

        collisions = coll_group(boxes, pipes, ground_blocks, flagpole, enemies)
        self.__adjust_after_y_collisions(labels, *collisions)

        # Powerup collision
        powerup, = coll_group(powerups)
        self.__adjust_after_powerup_collisions(labels, powerup)

    def __adjust_after_x_collisions(self, labels, box, pipe, ground, flagpole, enemy):
        '''Makes adjustments after Mario's x collisions'''
        def adjust_after_solid_collision(sprite):
            if self.vel.x > 0:              
                self.rect.right = sprite.rect.left
            elif self.vel.x < 0:
                self.rect.left = sprite.rect.right
            self.pos.x = self.rect.centerx

        if ground:
            adjust_after_solid_collision(ground)
        if pipe:
            adjust_after_solid_collision(pipe)
        if box:
            adjust_after_solid_collision(box)
        if flagpole and not isinstance(flagpole, QuestionBox):
            adjust_after_solid_collision(flagpole)
            self.transition_timer = pg.time.get_ticks()
            self.is_transition = True
            self.state = POLE_SLIDING

        if enemy and pg.sprite.collide_mask(self, enemy):
            if enemy.state != FLIPPED and enemy.state != DYING:
                if self.has_star:
                    enemy.state = FLIPPED
                    enemy.vel.y = -10
                    enemy.vel.x = 0.3 * self.vel.x 

                    # Create score label
                    score_label = lbl.ScoreLabel('1000', enemy.rect.centerx, enemy.rect.centery)
                    labels.append(score_label)
                    self.score += 1000
                    self.hit_enemy_sound.play()
                elif self.is_large and self.pow == NO_POW and self.vel.y < 0 and not self.is_invincible:
                    self.state = LARGE_TO_SMALL
                    self.transition_timer = pg.time.get_ticks()
                    self.is_transition = True
                    self.shrink_sound.play()
                elif self.pow == FIRE and self.vel.y < 0 and not self.is_invincible:
                    self.state = FIRE_TO_LARGE
                    self.transition_timer = pg.time.get_ticks()
                    self.is_transition = True
                    self.shrink_sound.play()
                elif not self.is_large and not self.is_invincible:
                    self.lives -= 1

    def __adjust_after_y_collisions(self, labels, box, pipe, ground, flagpole, enemy):
        '''Makes adjustments after Mario's y collisions'''
        def adjust_after_solid_collision(sprite, box_hit=None):
            if self.vel.y > 0:
                self.rect.bottom = sprite.rect.top
                self.state = RESTING
                self.gravity = GRAVITY
                self.acc.y = 0
                self.is_jumping = False
                self.vel.y = 0
            elif self.vel.y < 0:
                self.rect.top = sprite.rect.bottom
                self.is_falling = True
                self.vel.y = 2
                self.acc.y = self.gravity

                if box_hit:
                    if isinstance(sprite, QuestionBox) and sprite.state == CLOSED :
                        sprite.state = BUMPED

                    elif isinstance(sprite, Brick) and sprite.state == CLOSED:
                        sprite.state = BUMPED
            
            self.pos.y = self.rect.bottom

        if ground:
            adjust_after_solid_collision(ground)
        if pipe:
            adjust_after_solid_collision(pipe)
        if box:
            adjust_after_solid_collision(box, 'box')
        if flagpole and not isinstance(flagpole, QuestionBox):
            adjust_after_solid_collision(flagpole)
            self.transition_timer = pg.time.get_ticks()
            self.is_transition = True
            self.state = POLE_SLIDING

        if enemy and pg.sprite.collide_mask(self, enemy):
            if enemy.state != FLIPPED and enemy.state != DYING:
                if self.has_star:
                    enemy.state = FLIPPED
                    enemy.vel.y = -10
                    enemy.vel.x = 0.3 * self.vel.x 
                    self.hit_enemy_sound.play()
                elif self.vel.y > 0:
                    # Collision at player's feet
                    if isinstance(enemy, Goomba):
                        if enemy.state != DYING:
                            self.rect.bottom = enemy.rect.top
                            self.vel.y = GOOMBA_JUMP_VEL_Y

                            # Create score label
                            score_label = lbl.ScoreLabel('1000', enemy.rect.centerx, enemy.rect.centery)
                            labels.append(score_label)
                            self.score += 1000

                        enemy.kill_timer = pg.time.get_ticks()
                        enemy.state = DYING
                elif self.is_large and self.pow == NO_POW:
                    self.state = LARGE_TO_SMALL
                    self.transition_timer = pg.time.get_ticks()
                    self.is_transition = True
                    self.shrink_sound.play()
                elif self.pow == FIRE:
                    self.state = FIRE_TO_LARGE
                    self.transition_timer = pg.time.get_ticks()
                    self.is_transition = True
                    self.shrink_sound.play()               
            
            self.pos.y = self.rect.bottom

    def __adjust_after_powerup_collisions(self, labels, powerup):
        '''Checks for collisions with powerups'''
        if powerup and pg.sprite.collide_mask(self, powerup):
            powerup.kill()
            if isinstance(powerup, Mushroom):
                if not self.is_large:
                    self.is_large = True
                    self.transition_timer = pg.time.get_ticks()  # Set the time of getting mushroom
                    self.state = GROWING_LARGE
                    self.is_transition = True
                    self.grow_large_sound.play()
            elif isinstance(powerup, FireFlower):
                if self.pow != FIRE:
                    self.pow = FIRE
                    self.is_large = True
                    self.transition_timer = pg.time.get_ticks()
                    self.is_transition = True
                    self.state = LARGE_TO_FIRE
                    self.grow_large_sound.play()
            elif isinstance(powerup, Star):
                self.has_star = True     
                self.invincible_begin_timer = pg.time.get_ticks() 
                self.song_is_playing = True
                pg.mixer.music.load(MUSIC['star_music'])
                pg.mixer.music.play(3, 0.0)

            # Add 1000 points to score and spawn label
            score_label = lbl.ScoreLabel('1000', powerup.rect.x, powerup.rect.y)
            labels.append(score_label)
            self.score += 1000

    def __animation_delay(self):
        '''Calculates and returns the animation delay in ms based on mario's x velocity'''
        # animation delay = k*x-speed. Higher value of k--> faster rate of switching images
        an_delay = 100
        if self.vel.x != 0:
            an_delay -= abs(self.vel.x) * 10
       
        return an_delay
    
    def __update_image_index(self):
        '''Updates the image index'''
        if self.state == SLIDING:
            self.image_index = 5

        elif self.image_index == 0 and self.state != JUMPING:
            self.image_index += 1
            self.walk_timer = self.current_timer

        elif self.image_index != 0 and self.state != JUMPING:
            if (self.current_timer - self.walk_timer >
                  self.__animation_delay()):
                if self.image_index < 3:
                    self.image_index += 1
                else:
                    self.image_index = 1

                self.walk_timer = self.current_timer
        
        elif self.state == JUMPING:
            self.image_index = 4
        
        if self.image_index == 4 and self.state != JUMPING:
            # only 4 images are walking images, reset image_index
            self.image_index = 0
    
    def __handle_images(self, current_time):
        '''Determines which image to display'''

        if self.is_large and self.pow != FIRE and not(self.has_star):
            self.image = self.normal_big_frames[self.dir][self.image_index]
        
        elif self.pow == FIRE and not(self.has_star):
            self.image = self.fire_frames[self.dir][self.image_index]
        
        elif self.has_star:
            if current_time - self.invincible_begin_timer < 10000:
                self.__star_animation(current_time, 30)
            elif current_time - self.invincible_begin_timer < 12000:
                self.__star_animation(current_time, 100)
                if not pg.mixer.music.get_busy():
                    pg.mixer.music.load(MUSIC['star_running_out'])
                    pg.mixer.music.play(0, 0.0)
            else:
                self.has_star = False
                self.is_invincible = False

        else:
            self.image = self.normal_small_frames[self.dir][self.image_index]
        
    def __check_actions(self, keys, current_time):
        '''Check's key events'''
        
        if not keys[pg.K_SPACE]:
            self.allow_jump = True

        # Check walking
        if keys[pg.K_LEFT] and self.rect.left > 10:
            # Walk left
            if self.vel.x > 0 and self.state != JUMPING and self.state != FALLING:
                self.state = SLIDING
                self.acc.x = -TURN_ACC
            else:
                self.acc.x = -X_ACC
                self.dir = LEFT
            self.is_walking = True

        elif keys[pg.K_RIGHT] and self.rect.right < WIDTH - 10:
            # Walk right
            if self.vel.x < 0 and self.state != JUMPING and self.state != FALLING:
                self.state = SLIDING
                self.acc.x = TURN_ACC
            else:
                self.acc.x = X_ACC
                self.dir = RIGHT
            self.is_walking = True
            
        else: 
            # Standing still
            self.is_walking = False
            self.image_index = 0

        # Checks if player is able to jump
        if self.state == RESTING or self.state == SLIDING:
            if keys[pg.K_SPACE]:
                if self.allow_jump and self.vel.y == 0:
                    if self.is_large:    
                        self.jump_large_sound.play()
                    else:
                        self.jump_small_sound.play()
                    self.image_index = 0
                    self.__jump()

        # Fireball throw
        if keys[pg.K_f] and self.pow == FIRE:
            # Mario can only shoot a fireball every 300 ms     
            if current_time - self.fireball_shot > 300:
                self.fireball_shot = pg.time.get_ticks()
                if self.dir == RIGHT:
                    self.fireballs.add(Fireball(self.rect.right, self.rect.centery, self.dir))
                else:
                    self.fireballs.add(Fireball(self.rect.left, self.rect.centery, self.dir))
                self.fire_sound.play()
    
    def __jumping(self, keys):
        '''Called when mario is in a JUMPING state'''
        self.gravity = JUMP_GRAVITY
        self.allow_jump = False

        if self.vel.y >= 0 or not keys[pg.K_SPACE]:
            self.state = FALLING
            self.gravity = GRAVITY
        
    def __set_acc_and_vel(self):
        '''Updates mario's acceleration and velocity'''
        self.acc.x += self.vel.x * STAR_FRICTION if self.has_star else self.vel.x * FRICTION        
        self.vel.x += self.acc.x

        if self.vel.y < MAX_VEL_Y:
            # If max y speed has not been achieved
            self.vel.y += self.acc.y
