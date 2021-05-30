'''States for Powerups'''

REVEAL    = 0
ACTIVATED = 1
SPAWNING  = 2

MUSHROOM  = 2

STAR_DURATION = 10000   # 10 sec

# States for blocks
CLOSED   = 'closed'
BUMPED   = 'bumped'
MOVING   = 'moving'
OPENED   = 'opened'
BREAKING = 'breaking'


# Block velocities
QBOX_BUMP_VEL  = -5
BRICK_BUMP_VEL = -5

# Brick piece velocities
HIGH_BRICK_PIECE_VEL_Y = -10
MED_BRICK_PIECE_VEL_Y  = -7
LOW_BRICK_PIECE_VEL_Y  = -4
HIGH_BRICK_PIECE_VEL_X = 3
LOW_BRICK_PIECE_VEL_X  = 2


# Brick pieces

BRICK_PIECE_GRAVITY = .5
BRICK_PIECE_SCALAR = 1.3

TOP_LEFT     = 'topleft'
TOP_RIGHT    = 'topright'
BOTTOM_LEFT  = 'bottomleft'
BOTTOM_RIGHT = 'bottomright'

