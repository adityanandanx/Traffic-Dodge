# IMPORTS
import pygame as pg
import random
from settings import *
vec = pg.math.Vector2


class Player(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load('lembo.png')
        # self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.pos = vec(WW/2, WH)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.midtop = self.pos
        self.score = 0

    def update(self):
        # Initialize
        self.acc = vec(0, 0)
        self.vel = vec(0, 0)

        # Controls
        keys = pg.key.get_pressed()
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vel.x = 5
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vel.x = -5
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.acc.y = -2.5
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.acc.y = 1.5

        # Motion
        self.vel += self.acc
        self.pos += self.vel + self.acc/2
        self.rect.midtop = self.pos

        # Bounds
        if self.pos.x >= WW - self.rect.width/2:
            self.pos.x = WW - self.rect.width/2
        if self.pos.x <= self.rect.width/2:
            self.pos.x = self.rect.width/2
        if self.pos.y >= WH - self.rect.height:
            self.pos.y = WH - self.rect.height
        if self.pos.y <= 0:
            self.pos.y = 0


class Vehicles(pg.sprite.Sprite):
    def __init__(self, vel, pos):
        pg.sprite.Sprite.__init__(self)
        self.images = [pg.image.load('porshe.png'),
                       pg.image.load('lembo.png'),
                       pg.image.load('jeep.png')]
        self.image = self.images[random.randint(0, 2)]
        self.image = pg.transform.rotate(self.image, 180)
        self.rect = self.image.get_rect()
        self.pos = vec(*pos)
        self.vel = vec(0, vel)
        self.rect.midbottom = self.pos

    def update(self):
        global pscore
        self.pos.y += self.vel.y
        self.rect.midbottom = self.pos
        if self.pos.y > WH + 50:
            pscore += 1
            self.kill()


class BackGround(pg.sprite.Sprite):
    def __init__(self, color):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((WW, WH))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)


class Button(pg.sprite.Sprite):
    def __init__(self, imgloc, size, pos):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(imgloc)
        self.image = pg.transform.scale(self.image, size)
        self.rect = self.image.get_rect()
        self.size = vec(size)
        self.cpos = vec(pos)
        self.rect.center = self.cpos
        self.pos = vec(self.rect.topleft)


class MouseSprite(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((10, 10))
        self.image.fill((0, 0, 0, 0))
        self.rect = self.image.get_rect()
        self.pos = vec(*pg.mouse.get_pos())

    def update(self):
        self.pos = vec(*pg.mouse.get_pos())
        self.rect.center = self.pos
        self.pressedL = list(pg.mouse.get_pressed())[0]
        self.pressedM = list(pg.mouse.get_pressed())[1]
        self.pressedR = list(pg.mouse.get_pressed())[2]

    def is_pressed(self, group):
        clicks = pg.sprite.spritecollide(self, group, False)
        if clicks:
            if self.pressedL:
                return True

class Road(pg.sprite.Sprite):
    def __init__(self, pos):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load('road.png').convert()
        self.image = pg.transform.scale(self.image, (WW, WH))
        self.rect = self.image.get_rect()
        self.pos = vec(*pos)

    def update(self):

        self.rect.topleft = self.pos


class simple_sprite(pg.sprite.Sprite):
    def __init__(self, imgloc, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(imgloc)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


def scroll(sprite1, sprite2):
    sprite1.pos.y += 2
    sprite2.pos.y += 2
    if sprite1.pos.y >= WH:
        sprite1.pos.y = 0
    if sprite2.pos.y >= 0:
        sprite2.pos.y = -WH
