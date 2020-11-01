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
        super().__init__(10, pym.inf)
        if duck: #creates smaller player when ducking
            self.shape = pym.Poly.create_box(self, size= (40,40))
            self.position = 200, 40
        else:
            self.shape = pym.Poly(self, ((0,32), (0,54), (44,88), (84,88), (84,64), (48,0), (18,0)))
            self.position = 200, 60
        self.shape.elasticity = 0.0001
        space.add(self, self.shape)

enemy_types = [(160,80), (40, 80), (40, 40), (40, 40), (120, 40)]

class Enemy(pym.Body):
    def __init__(self, space):
        super().__init__(10, pym.inf, 1) # 1 means body type KINEMATIC
        global enemy_types
        a = random.randint(0, 4) #chooses one of the 5 enemy types
        if a == 0 or a == 1: #gives the enemy a different position according to its height
            self.position = 1280, 60
        else:
            self.position = 1280, 40
        self.velocity = -200, 0 #in future versions the speed will change as the difficulty increases
        self.shape = pym.Poly.create_box(self, enemy_types[a])
        self.shape.elasticity = 0.0001
        space.add(self, self.shape)

class Ground(pym.Body):
    def __init__(self, space):
        super().__init__(10, pym.inf, 2) #2 means body type STATIC
        self.position = 0, 0
        self.shape = pym.Poly.create_box(self, (2700, 40))
        self.shape.elasticity = 0.0001
        space.add(self, self.shape)

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

        self.player = Player(self.space, False)
        self.ground = Ground(self.space)

        self.sleep = 30 #30 frames untill first enemy
        self.doing_duck = False
        self.doing_jump = False
        
        self.jumping_image = pyg.image.load("sprites/kostium3.png")
        self.jumping_sprite = pyg.sprite.Sprite(self.jumping_image)
        self.walking_images = [pyg.image.load("sprites/kostium3.png"),pyg.image.load("sprites/kostium5.png"),pyg.image.load("sprites/kostium3.png"),pyg.image.load("sprites/kostium6.png")]
        self.walking_animation = pyg.image.Animation.from_image_sequence(self.walking_images, duration= 0.075, loop= True)
        self.walking_sprite = pyg.sprite.Sprite(self.walking_animation)
        self.ducking_images = [pyg.image.load("sprites/kostium7.png"),pyg.image.load("sprites/kostium8.png"),pyg.image.load("sprites/kostium7.png"),pyg.image.load("sprites/kostium9.png")]
        self.ducking_animation = pyg.image.Animation.from_image_sequence(self.ducking_images, duration= 0.075, loop= True)
        self.ducking_sprite = pyg.sprite.Sprite(self.ducking_animation)
    
    def on_draw(self):
        self.clear()
        self.space.debug_draw(self.options) #drawing the pymunk space in pyglet
        self.fps.draw()
        if self.doing_jump :
            self.jumping_sprite.draw()
        if self.doing_duck :
            self.ducking_sprite.draw()
        elif not self.doing_jump and not self.doing_duck :
            self.walking_sprite.draw()

    def on_key_press(self, symbol, modifiers):
#The player can only begin an action when he is on the ground, we check this using his y coordinate (rounded to 10)
        if round(self.player.position[1]/10)*10 == 60: 
            if symbol == key.SPACE or symbol == key.UP:
                self.doing_jump = True #see key release
                self.player.velocity = 0, 700
            elif symbol == key.DOWN:
                self.doing_duck = True #see key release
                self.space.remove(self.player.shape) #deletes the player, to then create a smaller one
                self.player = Player(self.space, True)

    def on_key_release(self, symbol, modifiers):
        if symbol == key.SPACE or symbol == key.UP:
#checks if the player was allowed to jump/duck. If the player hit and release a key in the air, nothing happens
            if self.doing_jump and self.player.velocity[1] > 0: #checks if player isn't already falling
                self.doing_jump = False
                self.player.velocity = 0, 0
        if symbol == key.DOWN and self.doing_duck:
            self.doing_duck = False
            self.space.remove(self.player.shape) #deletes small player and creates a new, normally sized one
            self.player = Player(self.space, False)

    def update(self, dt): #date and time
        self.space.step(dt) #steps every frame
        self.sleep -= 1
        self.walking_sprite.position = self.player.position
        self.jumping_sprite.position = self.player.position
        if self.sleep == 0:
            self.sleep = random.randint(90, 150) #random sleep time intil new enemy is generated
            self.enemy = Enemy(self.space)
        
        
    

window = Window(1280, 720, 'Pymunk', resizable=False)
pyg.clock.schedule_interval(window.update, 1/60) #60 frames per second
pyg.app.run()