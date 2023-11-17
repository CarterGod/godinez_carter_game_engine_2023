# This file was created by Carter Godinez

# import libraries and modules
import pygame as pg
from pygame.sprite import Sprite

from pygame.math import Vector2 as vec
import os
# import all settings
from settings import *

# setup asset folders here - images sounds etc.
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'images')
snd_folder = os.path.join(game_folder, 'sounds')

class Player(Sprite):
    def __init__(self, game):
        Sprite.__init__(self)
        self.game = game
        # import Ramzey image as player
        self.image = pg.image.load(os.path.join(img_folder, 'Ramzey.png')).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (0, 0)
        # put player in center of screen
        self.pos = vec(WIDTH/2, HEIGHT/2)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        # assign player hitpoints
        self.hitpoints = 100
    def controls(self):
        # allow player to move and jump
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.acc.x = -5
        if keys[pg.K_d]:
            self.acc.x = 5
        if keys[pg.K_SPACE]:
            self.jump()
    def jump(self):
        hits = pg.sprite.spritecollide(self, self.game.all_platforms, False)
        if hits:
            self.vel.y = -PLAYER_JUMP
    def update(self):
        # CHECKING FOR COLLISION WITH MOBS HERE>>>>>
        self.acc = vec(0,PLAYER_GRAV)
        self.controls()
        # if friction - apply here
        self.acc.x += self.vel.x * -PLAYER_FRIC
        # self.acc.y += self.vel.y * -0.3
        # equations of motion
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.rect.midbottom = self.pos
        # define what happens when mobs collide with player
        mobcollide = pg.sprite.spritecollide(self, self.game.all_mobs, True)
        # if they collide, the player loses 10 hitpoints
        if mobcollide:
            self.hitpoints -= 10
        # define what happens when the player reaches 0 hitpoints
        if self.hitpoints == 0:
            # the player is no longer visible
            self.image.fill(BLACK)
        # assign variable to collision between player and power up
        powerupcollide = pg.sprite.spritecollide(self, self.game.all_powerups, True)
        # if they collide, the player gains 50 hp
        if powerupcollide:
            self.hitpoints += 50

# platforms
class Platform(Sprite):
    def __init__(self, x, y, w, h, category):
        Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        # set color of platforms to green
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.category = category
        self.speed = 0
        # set initial speed if platform is set as "moving"
        if self.category == "moving":
            self.speed = 5
    def update(self):
        # define what happens if platform has category "moving"
        if self.category == "moving":
            self.rect.x += self.speed
            if self.rect.x + self.rect.w > WIDTH or self.rect.x < 0:
                self.speed = -self.speed

# mobs
class Mob(Sprite):
    def __init__(self, x, y, w, h, category):
        Sprite.__init__(self)
        # import Greg image as mob
        self.image = pg.image.load(os.path.join(img_folder, 'Greg.png')).convert()
        self.image.set_colorkey(BLACK)
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
        # when mobs reach bottom of screen, put them back at top
        if self.rect.y > HEIGHT:
            self.rect.y = 0

class PowerUp(Sprite):
    def __init__(self, x, y, w, h, category):
        Sprite.__init__(self)
        # import heart image as powerup
        self.image = pg.image.load(os.path.join(img_folder, 'heart.png')).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        print(self.rect.center)
        self.category = category
        self.speed = 0
        if self.category == "moving":
            self.speed = 6
    def update(self):
        if self.category == "moving":
            self.rect.x += self.speed
            if self.rect.x + self.rect.w > WIDTH or self.rect.x < 0:
                self.speed = -self.speed
        
