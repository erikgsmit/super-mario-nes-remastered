'''Constants for entities'''

MARIO_START_X = 50
GROUND = 527            # Ground y position

# Player constants
GRAVITY      = 1.0         # Gravity acceleration
JUMP_GRAVITY = 0.32
X_ACC        = 0.4
TURN_ACC     = 0.2
FRICTION     = -0.09       # Friction in x-direction
JUMP_VEL     = -11         # Initial jump velocity
MAX_VEL_Y    = 10          # Maximum falling velocity
GOOMBA_FALL_GRAVITY = 0.8

STAR_JUMP_VEL = JUMP_VEL - 1
STAR_FRICTION = -0.07

SLIDING_VEL = 3

GOOMBA_JUMP_VEL_Y = -8

STARTING_LIVES = 3

PLAYER_SCALAR = 2.2

# Enemy constants
ENEMY_VEL_X = 1.1

# Powerup constants
MUSHROOM_VEL_X = 2
FIREBALL_VEL_X = 6.5
FIREBALL_BOUNCE_VEL_Y = -7
COIN_VEL_Y = -15

# Player directions
RIGHT = 0
LEFT  = 1
STILL = 3

# Mario States
POLE_SLIDING = 'pole-sliding'
END = 'end'
RESTING = 'resting'
FALLING = 'falling'
JUMPING = 'jumping'
SLIDING = 'sliding'
GROWING_LARGE = 'growing_large'
LARGE_TO_SMALL = 'large_to_small'
LARGE_TO_FIRE = 'large_to_fire'
FIRE_TO_LARGE = 'fire_to_large'

# Powerup states
NO_POW = 0
FIRE   = 2  # After picking up fire flower

#Star values
STAR_VEL_Y = 5
STAR_VEL_X = 3
STAR_GRAVITY = 0.2


# Enemy States
ACTIVATED   = 0
DEACTIVATED = 1
ALIVE       = 2
JUMPED_ON   = 3
DYING       = 4
FLIPPED     = 5

# Mario sizes
DEFAULT_SIZE = (64,64)
TEMP_SIZE    = (82,82)   # Size only exist when mario goes from small to large
LARGE_SIZE   = (100,100)


# Pipe stuff
TALL  = 0
SHORT = 1

# Flagpole
FLAG_POLE_SCALAR = 0.3
FLAG_VEL_Y = 2
FLAG_DOWN_Y = 447