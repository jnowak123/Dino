import pymunkoptions
pymunkoptions.options['debug'] = False #removes pymunk debug print from console
import pyglet as pyg
import pymunk as pym
from pymunk.pyglet_util import DrawOptions
from pyglet.window import FPSDisplay, key

class Player(pym.Body):
    def __init__(self, space):
        super().__init__(10, pym.inf) #infinite moment => doesn't roll
        self.position = 200, 140
        shape = pym.Poly.create_box(self, (40, 80))
        shape.elasticity = 0
        space.add(self, shape)

class Ground(pym.Body):
    def __init__(self, space):
        super().__init__(10, pym.inf, pym.Body.STATIC) #static body => no gravity effect or moving at all
        self.position = 0, 0
        shape = pym.Poly.create_box(self, (2700, 40))
        shape.elasticity = 0
        space.add(self, shape)

class Window(pyg.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_location(30, 50) #window position
        self.fps = FPSDisplay(self)

        self.space = pym.Space() #pymunk space
        self.space.gravity = 0, -900
        self.options = DrawOptions()

        self.player = Player(self.space)
        self.ground = Ground(self.space)

    def on_draw(self):
        self.clear()
        self.space.debug_draw(self.options) #drawing the pymunk space
        self.fps.draw()

    def on_key_press(self, symbol, modifiers):
        if symbol == key.SPACE:
            self.player.velocity = 0, 600

    def update(self, dt): #date and time
        self.space.step(dt)

window = Window(1280, 720, "Pymunk", resizable=False)
pyg.clock.schedule_interval(window.update, 1/60)
pyg.app.run()