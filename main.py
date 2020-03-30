# IMPORTS
from settings import *
from sprites import *
import pygame as pg
pg.init()


class Game:
    def __init__(self, id):
        pg.init()
        pg.display.set_caption(TITLE)
        self.window = pg.display.set_mode((WW, WH))
        self.running = True
        self.clock = pg.time.Clock()
        self.all_sprites = pg.sprite.Group()
        self.vehicles = pg.sprite.Group()
        self.playing = False
        self.ticks = 0      # Initial value of timer

    def new(self):
        # Road
        self.r1 = Road((0, 0))
        self.r2 = Road((0, -WH))
        self.all_sprites.add(self.r1, self.r2)
        # Player
        self.player = Player()
        self.all_sprites.add(self.player)
        # Run
        self.run()

    def run(self):
        while self.playing:
            self.events()
            self.draw()
            self.update()
            self.ticks += 1     # Timer increment

    def draw(self):
        self.window.fill(GREEN)
        self.all_sprites.sprites()
        self.all_sprites.draw(self.window)

    def update(self):
        # FPS
        self.clock.tick(FPS)

        # Spawning Vehicles
        if self.ticks % random.randint(20, 100) == 0:
            veh = Vehicles(random.randint(2, 5), (random.randrange(20, WW, 50), 0))
            self.all_sprites.add(veh)
            self.vehicles.add(veh)

        # Collision
        hits = pg.sprite.spritecollide(self.player, self.vehicles, True)
        if hits:
            self.all_sprites.empty()
            self.vehicles.empty()
            self.playing = False

        # road
        scroll(self.r1, self.r2)
        # Updating
        self.all_sprites.update()
        pg.display.flip()

    def events(self):
        for e in pg.event.get():
            if e.type == pg.QUIT:
                self.running = False
                self.playing = False

    def show_start(self):
        # Mouse
        m = MouseSprite()
        # sprites group of SS
        start_scr_sprites = pg.sprite.Group()
        start_scr_buttons = pg.sprite.Group()
        # Background
        bg = BackGround(WHITE)
        start_scr_sprites.add(bg)
        # Title
        t = simple_sprite('trafficdodge.png', WW/2, 200)
        start_scr_sprites.add(t)
        # Button
        bt = Button('play.png', (250, 100), vec(WW/2, 400))
        start_scr_sprites.add(bt)
        start_scr_buttons.add(bt)
        showing = True
        while showing:

            for e in pg.event.get():
                if e.type == pg.QUIT:
                    showing = False
                    self.running = False

            start_scr_sprites.draw(self.window)
            if m.is_pressed(start_scr_buttons):
                self.playing = True
                showing = False
                # self.new()
            start_scr_sprites.update()
            m.update()
            pg.display.update()


    def show_over(self):
        all_sprites = pg.sprite.Group()
        buttons = pg.sprite.Group()
        # Mouse
        m1 = MouseSprite()
        # Background
        bg = BackGround(WHITE)
        all_sprites.add(bg)
        # Title
        t = simple_sprite('trafficdodge.png', WW/2, 200)
        all_sprites.add(t)
        # Buttons
        replay_bt = Button('replay.png', (100, 100), (WW/2, 400))
        all_sprites.add(replay_bt)
        buttons.add(replay_bt)
        showing = True
        while showing:
            # QUIT
            for e in pg.event.get():
                if e.type == pg.QUIT:
                    showing = False
                    self.running = False
            # Draw
            all_sprites.draw(self.window)
            # Press
            if m1.is_pressed(buttons):
                self.playing = True
                showing = False
                self.all_sprites.empty()
            # Update
            all_sprites.update()
            m1.update()
            pg.display.update()

g = Game(1)

g.show_start()
while g.running:
    g.new()
    if g.running:
        g.show_over()

pg.quit()
