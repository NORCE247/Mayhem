"""Authors: Narongchai Cherdchoo & Daniels Sliks, 2024."""
# SETTING
import pygame

SHOW_FPS = False
DEBUG_MODE = False

# BACKGROUND
RESOLUTION = (1000, 800)
BACKGROUND_COLOR = (120, 180, 200)
FPS = 60

# PLAYER
G_ACCELERATION = 9.8/FPS
SPEED_ACCELERATION = 0.5
AIR_FRICTION = 0.1
TERMINAL_VELOCITY = 7
MAX_SPEED = 7
HP = 1000
FUEL = 10000
MAX_LANDING_ANGLE = 40
MAX_LANDING_SPEED = 3
RESPAWN_POINT = [[150, 750], [850, 750]]
SIZE = [15, 20]
COLOR = ("black")

# WEAPON
SHOOT_COOLDOWN = 30
BULLET_SPEED = 10
MAX_TRAVEL_DISTANCE = 100
BULLET_SIZE = 10

# PLAYER 1 CONTROLS
LEFT_KEY_P1 = pygame.K_a
RIGHT_KEY_P1 = pygame.K_d
POWER_KEY_P1 = pygame.K_w
SHOOT_KEY_P1 = pygame.K_s

# PLAYER 2 CONTROLS
LEFT_KEY_P2 = pygame.K_LEFT
RIGHT_KEY_P2 = pygame.K_RIGHT
POWER_KEY_P2 = pygame.K_UP
SHOOT_KEY_P2 = pygame.K_DOWN

PLAYER_CONTROLS = [[POWER_KEY_P1, LEFT_KEY_P1, RIGHT_KEY_P1, SHOOT_KEY_P1],
                   [POWER_KEY_P2, LEFT_KEY_P2, RIGHT_KEY_P2, SHOOT_KEY_P2]]