import pymunkoptions
pymunkoptions.options['debug'] = False #removes pymunk debug print from console
import random
import pyglet as pyg
import pymunk as pym
from pymunk.pyglet_util import DrawOptions
from pyglet.window import FPSDisplay, key
from pyglet.gl import glClearColor

class Player(pym.Body):
    def __init__(self, space, duck):
        super().__init__(10, pym.inf) #infinite moment => doesn't roll
        if duck:
            self.shape = pym.Poly.create_box(self, (40, 40))
            self.position = 200, 40
        else:
            self.shape = pym.Poly.create_box(self, (40, 80))
            self.position = 200, 60
        self.elasticity = 0.0
        space.add(self, self.shape)

enemy_types = [(160,80), (40, 80), (40, 40), (40, 40), (120, 40)]

class Enemy(pym.Body):
    def __init__(self, space):
        super().__init__(10, pym.inf, 1)
        global enemy_types
        a = random.randint(0, 4)
        if a == 0 or a == 1:
            self.position = 1280, 60
        else:
            self.position = 1280, 40
        self.velocity = -200, 0 # in the future, velocity will be equal to speed
        shape = pym.Poly.create_box(self, enemy_types[a])
        self.elasticity = 0.0
        space.add(self, shape)

class Ground(pym.Body):
    def __init__(self, space):
        super().__init__(10, pym.inf, pym.Body.STATIC) #static body => no gravity effect or moving at all
        self.position = 0, 0
        shape = pym.Poly.create_box(self, (2700, 40))
        self.elasticity = 0.0
        space.add(self, shape)

class Window(pyg.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        pyg.gl.glClearColor(1000,1000,1000,1000) #background colour
        self.set_location(30, 50) #window position
        self.fps = FPSDisplay(self)

        self.space = pym.Space() #pymunk space
        self.space.gravity = 0, -900
        self.options = DrawOptions()
        self.space.iterations = 250

        self.player = Player(self.space, False)
        self.ground = Ground(self.space)

        self.sleep = 30
        self.doing_duck = False

    def position(self, body, dt):
        pass

    def on_draw(self):
        self.clear()
        self.space.debug_draw(self.options) #drawing the pymunk space
        self.fps.draw()

    def on_key_press(self, symbol, modifiers):
        if round(self.player.position[1]/10)*10 == 60:
            if symbol == key.SPACE or symbol == key.UP:
                self.player.velocity = 0, 600
            elif symbol == key.DOWN:
                self.doing_duck = True
                self.space.remove(self.player.shape)
                self.player = Player(self.space, True)

    def on_key_release(self, symbol, modifiers):
        if symbol == key.SPACE or symbol == key.UP:
            if self.player.velocity[1] > 0:
                self.player.velocity = 0, 0
        if symbol == key.DOWN and self.doing_duck:
            self.doing_duck = False
            self.space.remove(self.player.shape)
            self.player = Player(self.space, False)

    def update(self, dt): #date and time
        self.space.step(dt)
        self.sleep -= 1
        if self.sleep == 0:
            self.sleep = random.randint(90, 150) # enemy generate
            self.enemy = Enemy(self.space)
    



window = Window(1280, 720, 'Pymunk', resizable=False)
pyg.clock.schedule_interval(window.update, 1/60)
pyg.app.run()