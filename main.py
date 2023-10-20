# content from kids can code: http://kidscancode.org/blog/

# import libraries and modules
import pygame as pg
from pygame.sprite import Sprite
import random
from random import randint
import os

vec = pg.math.Vector2

# setup asset folders here - images sounds etc.
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'images')
snd_folder = os.path.join(game_folder, 'sounds')

# game settings 
WIDTH = 360
HEIGHT = 480
FPS = 30
SCORE = 0

# player settings
PLAYER_JUMP = 30
PLAYER_GRAV = 1.5

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
SKYBLUE = (150, 200, 255)

def draw_text(text, size, color, x, y):
    font_name = pg.font.match_font('arial')
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    screen.blit(text_surface, text_rect)

class Player(Sprite):
    # this is the init method where you can setup properties for a class
    def __init__(self):
        # call the super class init method
        Sprite.__init__(self)
        # self.image = pg.Surface((50, 50))
        # self.image.fill(GREEN)
        # use an image for player sprite...
        self.image = pg.image.load(os.path.join(img_folder, 'theBell.png')).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.pos = vec(WIDTH/2, HEIGHT/2)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.cofric = -0.3
        self.hitpoints = 100
    def controls(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.acc.x = -5
        if keys[pg.K_d]:
            self.acc.x = 5
        if keys[pg.K_SPACE]:
            self.jump()
    def jump(self):
        hits = pg.sprite.spritecollide(self, all_platforms, False)
        if hits:
            print("i can jump")
            self.vel.y = -PLAYER_JUMP
    def update(self):
        self.acc = vec(0,PLAYER_GRAV)
        self.controls()
        # friction for side to side 
        self.acc.x += self.vel.x * self.cofric

        # equations of motion
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        self.rect.midbottom = self.pos
        # check to see if he fell off the bottom
        if self.rect.y > HEIGHT:
            self.pos = vec(WIDTH/2, HEIGHT/2)
            


# platforms

class Platform(Sprite):
    def __init__(self, x, y, w, h, category):
        Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        print(self.rect.center)
        self.category = category
        self.speed = 10
    def update(self):
        if self.category == "moving":
            self.rect.x += self.speed
            if self.rect.x + self.rect.w > WIDTH or self.rect.x < 0:
                self.speed = -self.speed
        if self.category == "ice":
            self.image.fill(WHITE)

class Mob(Sprite):
    def __init__(self, x, y, w, h, category):
        Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        print(self.rect.center)
        self.category = category
        self.speed = 10
    def update(self):
        if self.category == "moving":
            self.rect.x += self.speed
            if self.rect.x + self.rect.w > WIDTH or self.rect.x < 0:
                self.speed = -self.speed
                self.rect.y += 25
        if self.category == "ice":
            self.image.fill(WHITE)

        if self.rect.y > HEIGHT:
            self.rect.y = 0
            # self.kill()
            # print("this happened")
            print(all_mobs)
     



# init pygame and create a window
pg.init()
pg.mixer.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("My Game...")
clock = pg.time.Clock()

# create a group for all sprites
all_sprites = pg.sprite.Group()
all_platforms = pg.sprite.Group()
all_mobs = pg.sprite.Group()

# instantiate classes
player = Player()
plat = Platform(150, 300, 100, 30, "ice")
plat1 = Platform(200, 200, 100, 30, "moving")





# add instances to groups
all_sprites.add(player)
all_sprites.add(plat)
all_sprites.add(plat1)
all_platforms.add(plat)
all_platforms.add(plat1)
for i in range(0,20):
    m = Mob(randint(0,WIDTH),randint(0,HEIGHT),25,25,"moving")
    all_sprites.add(m)
    all_mobs.add(m)

# Game loop
running = True



while running:
    # keep the loop running using clock
    currentfps = clock.tick(FPS)
        
    for event in pg.event.get():
        # check for closed window
        if event.type == pg.QUIT:
            running = False
    
    ############ Game Update Loop Section ##############
    # update all sprites
    # (the player controls or input happen in player update method)
    all_sprites.update()
    
    # this is what prevents the player from falling through the platform when falling down...
    if player.vel.y > 0:
            hits = pg.sprite.spritecollide(player, all_platforms, False)
            if hits:
                if hits[0].category == "moving":
                    player.vel.x = hits[0].speed*1.75

                player.pos.y = hits[0].rect.top
                player.vel.y = 0

                
                
    # this prevents the player from jumping up through a platform
    if player.vel.y < 0:
        hits = pg.sprite.spritecollide(player, all_platforms, False)
        if hits:
            print("ouch")
            SCORE -= 1
            if player.rect.bottom >= hits[0].rect.top - 5:
                player.rect.top = hits[0].rect.bottom
                player.acc.y = 5
                player.vel.y = 0

    mhits = pg.sprite.spritecollide(player, all_mobs, True)
    if mhits:
        player.hitpoints -= 1
        print(player.hitpoints)
    # if mhits:
    #     mhits[0].kill()
    #     print(all_mobs)
    ############ Draw ################
    # draw the background screen
    # draw all sprites
    screen.fill(SKYBLUE)
    all_sprites.draw(screen)
    draw_text("FPS: " + str(currentfps), 22, BLACK, WIDTH/2, HEIGHT/10)

    # buffer - after drawing everything, flip display
    pg.display.flip()

pg.quit()
