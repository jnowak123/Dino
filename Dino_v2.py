import pymunkoptions
pymunkoptions.options['debug'] = False #removes pymunk debug print from console
import random
import pyglet as pyg
import pymunk as pym
from pymunk.pyglet_util import DrawOptions
from pyglet.window import FPSDisplay, key
from pyglet.gl import glClearColor

class Game_Object(pym.Body):
    def __init__(self, space, sizex, sizey, posx, posy, velx, vely, body_type, image=None):
        if image:
            pass
        else:
            super().__init__(10, pym.inf, body_type)
            self.position = posx, posy
            self.velocity = velx, vely
            self.shape = pym.Poly.create_box(self, (sizex, sizey))
            self.shape.elasticity = 0.0
            space.add(self, self.shape)

enemy_types = [[160,80], [40, 80], [40, 40], [40, 40], [120, 40]]

class Window(pyg.window.Window):
    def __init__(self, *args, **kwargs): #arguments and keyword arguments
        super().__init__(*args, **kwargs)
        pyg.gl.glClearColor(1000,1000,1000,1000) #background colour
        self.set_location(30, 50) #window position
        self.fps = FPSDisplay(self)

        self.space = pym.Space() #pymunk space
        self.space.gravity = 0, -900 
        self.options = DrawOptions() #pymunk + pyglet integration
        self.space.iterations = 250 #how often a list checks if something should bounce

        self.player = Game_Object(self.space, 40, 80, 200, 60, 0, 0, 0)
        self.ground = Game_Object(self.space, 2700, 40, 0, 0, 0, 0, 2)

        self.sleep = 30 #30 frames untill first enemy
        self.doing_duck = False
        self.doing_jump = False

    def on_draw(self):
        self.clear()
        self.space.debug_draw(self.options) #drawing the pymunk space in pyglet
        self.fps.draw()

    def on_key_press(self, symbol, modifiers):
#The player can only begin an action when he is on the ground, we check this using his y coordinate (rounded to 10)
        if round(self.player.position[1]/10)*10 == 60: 
            if symbol == key.SPACE or symbol == key.UP:
                self.doing_jump = True #see key release
                self.player.velocity = 0, 700
            elif symbol == key.DOWN:
                self.doing_duck = True #see key release
                self.space.remove(self.player.shape) #deletes the player, to then create a smaller one
                self.player = Game_Object(self.space, 40, 40, 200, 40, 0, 0, 0)

    def on_key_release(self, symbol, modifiers):
        if symbol == key.SPACE or symbol == key.UP:
#checks if the player was allowed to jump/duck. If the player hit and release a key in the air, nothing happens
            if self.doing_jump and self.player.velocity[1] > 0: #checks if player isn't already falling
                self.doing_jump = False
                self.player.velocity = 0, 100
        if symbol == key.DOWN and self.doing_duck:
            self.doing_duck = False
            self.space.remove(self.player.shape) #deletes small player and creates a new, normally sized one
            self.player = Game_Object(self.space, 40, 80, 200, 60, 0, 0, 0)

    def update(self, dt): #date and time
        self.space.step(dt) #steps every frame
        self.sleep -= 1
        if self.sleep == 0:
            self.sleep = random.randint(90, 150) #random sleep time intil new enemy is generated
            x = random.randint(0,4)
            if x <= 1:
                self.enemy = Game_Object(self.space, enemy_types[x][0], enemy_types[x][1], 1280, 60, -200, 0, 1)
            else:
                self.enemy = Game_Object(self.space, enemy_types[x][0], enemy_types[x][1], 1280, 40, -200, 0, 1)
    

window = Window(1280, 720, 'Pymunk', resizable=False)
pyg.clock.schedule_interval(window.update, 1/60) #60 frames per second
pyg.app.run()