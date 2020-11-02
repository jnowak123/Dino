import pymunkoptions
pymunkoptions.options['debug'] = False #removes pymunk debug print from console
import random
import pyglet as pyg
import pymunk as pym
from pymunk.pyglet_util import DrawOptions
from pyglet.window import FPSDisplay, key
from pyglet.gl import glClearColor

class Game_Object(pym.Body):
    def __init__(self, space, sizex, sizey, posx, posy, velx, vely, body_type):
        super().__init__(10, pym.inf, body_type)
        self.position = posx, posy
        self.velocity = velx, vely
        self.shape = pym.Poly.create_box(self, (sizex, sizey))
        self.shape.elasticity = 0.0
        space.add(self, self.shape)

class Sprites():
    def __init__(self):
        pass

object_types = [[40, 80, 200, 60, 0, 0, 1], [40, 40, 200, 40, 0, 0, 1], [2700, 40, 0, 0, 0, 0, 2], #player, player ducking and ground
                [160,80,1280,60], [40, 80,1280,60], [40, 40,1280,40], [40, 40,1280,40], [120, 40,1280,40]] #cactuses

class Window(pyg.window.Window):
    def __init__(self, *args, **kwargs): #arguments and keyword arguments
        super().__init__(*args, **kwargs)
        pyg.gl.glClearColor(1000,1000,1000,1000) #background colour
        self.set_location(30, 50) #window position
        self.fps = FPSDisplay(self)

        self.space = pym.Space() #pymunk space
        self.options = DrawOptions() #pymunk + pyglet integration

        self.player = Game_Object(self.space, *object_types[0])
        self.ground = Game_Object(self.space, *object_types[2])

        self.sleep = 30 #30 frames untill first enemy
        self.state = None
        self.doing_jump = False

    def on_draw(self):
        self.clear()
        self.space.debug_draw(self.options) #drawing the pymunk space in pyglet
        self.fps.draw()

    def on_key_press(self, symbol, modifiers):
        if symbol == key.SPACE or symbol == key.UP:
            self.state = 'jumping'
        elif symbol == key.DOWN:
            self.doing_duck = True #see key release
            self.space.remove(self.player.shape) #deletes the player, to then create a smaller one
            self.player = Game_Object(self.space, *object_types[1])

    def on_key_release(self, symbol, modifiers):
        if symbol == key.SPACE or symbol == key.UP:
            self.state = 'falling'
        if symbol == key.DOWN and self.doing_duck:
            self.doing_duck = False
            self.space.remove(self.player.shape) #deletes small player and creates a new, normally sized one
            self.player = Game_Object(self.space, *object_types[0])

    def update(self, dt): #date and time
        self.space.step(dt) #steps every frame
        self.jump(self.player, self.state)
        self.enemy_generation()
        self.sprite_update()

    def jump (self, player, state=None):
        if state == 'jumping':
            player.velocity += 0, 100
        elif state == 'falling':
            player.velocity += 0, -10
        else:
            player.velocity = 0, 0

    def enemy_generation(self):
        self.sleep -= 1
        if self.sleep == 0:
            self.sleep = random.randint(90, 150) #random sleep time intil new enemy is generated
            x = random.randint(3,7)
            self.enemy = Game_Object(self.space, *object_types[x], -200, 0, 1)

    def sprite_update(self):
        pass

window = Window(1280, 720, 'Pymunk', resizable=False)
pyg.clock.schedule_interval(window.update, 1/60) #60 frames per second
pyg.app.run()