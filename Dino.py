import pymunkoptions
pymunkoptions.options['debug'] = False #removes pymunk debug print from console
import random
import pyglet as pyg
import pymunk as pym
from pymunk.pyglet_util import DrawOptions
from pyglet.window import FPSDisplay, key

def Player(space):
    body = pym.Body(10, pym.inf) #infinite moment => doesn't roll
    body.position = 200, 40
    shape = pym.Poly.create_box(body, (40, 80))
    shape.elasticity = 0
    space.add(body, shape)
    return body

enemy_types = [(160,80), (40, 80), (40, 40), (40, 40), (120, 40)]

def Enemy(space):
    body = pym.Body(10, pym.inf, 1)
    global enemy_types
    a = random.randint(0, 4)
    if a == 0 or a == 1:
        body.position = 1280, 60
    else:
        body.position = 1280, 40
    body.velocity = -200, 0 # in the future, velocity will be equal to speed
    body.elasticity = 0
    shape = pym.Poly.create_box(body, enemy_types[a])
    space.add(body, shape)

def Ground(space):
    body = pym.Body(10, pym.inf, pym.Body.STATIC) #static body => no gravity effect or moving at all
    body.position = 0, 0
    shape = pym.Poly.create_box(body, (2700, 40))
    shape.elasticity = 0
    space.add(body, shape)

window = pyg.window.Window(1280, 720, 'Dino', resizable=False)
window.set_location(30, 50)
options = DrawOptions()

space = pym.Space()
space.gravity = 0, -900

player = Player(space)
Ground(space)

@window.event
def on_draw():
    window.clear()
    space.debug_draw(options) #drawing the pymunk space

def on_key_press(symbol, modifiers):
    if symbol == key.SPACE or symbol == key.UP:
        pass

def update(dt): #date and time
    space.step(dt)
    a = random.randint(0, 80) # enemy generate
    if a == 1:
        Enemy(space)

pyg.clock.schedule_interval(update, 1/60)
pyg.app.run()