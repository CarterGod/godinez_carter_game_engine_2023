# This file was created by: Carter Godinez
# Content from Chris Bradfield; Kids Can Code
# KidsCanCode - Game Development with Pygame video series
# Video link: https://youtu.be/OmlQ0XCvIn0 

# game settings 
WIDTH = 720
HEIGHT = 720
FPS = 30

# player settings
PLAYER_JUMP = 30
PLAYER_GRAV = 2.5
PLAYER_FRIC = 0.2

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# define platforms
PLATFORM_LIST = [(0, HEIGHT * 3 / 4, 75, 20,"moving"),
                 (0, HEIGHT - 40, WIDTH, 40, "normal"),
                 (150, 120, 100, 20, "moving"),
                 (0, 250, 75, 20, "moving"),
                 (175, 400, 100, 20, "moving")]
