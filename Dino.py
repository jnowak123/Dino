import random
import pyglet as pyg
import pymunk as pym
from pymunk.pyglet_util import DrawOptions
from pyglet.window import FPSDisplay, key
from pyglet.gl import glClearColor
from pyglet import font
import os

# import pymunkoptions
# pymunkoptions.options['debug'] = False #removes pymunk debug print from console

class Player_Object(pym.Body): #class for creating all objects, in the future this will be replaced by sprites
    def __init__(self, space, vertices, posx, posy, velx, vely, body_type, name=None):
        super().__init__(10, pym.inf, body_type)
        self.position = posx, posy
        self.velocity = velx, vely
        self.shape = pym.Poly(self, vertices)
        self.shape.collision_type = name
        space.add(self, self.shape)

class Game_Object(pym.Body): #class for creating all objects, in the future this will be replaced by sprites
    def __init__(self, space, sizex, sizey, posx, posy, velx, vely, body_type, name=None):
        super().__init__(10, pym.inf, body_type)
        self.position = posx, posy
        self.velocity = velx, vely
        self.shape = pym.Poly.create_box(self, (sizex, sizey))
        self.shape.collision_type = name
        space.add(self, self.shape)
        
class Sprites(pyg.sprite.Sprite): #sprite class, todo
    def __init__(self, images, animation, position):      
        if animation :
            ani = pyg.image.Animation.from_image_sequence(images,duration= 0.075, loop=True)
            super().__init__(img = ani)
        else:
            super().__init__(images)
        self.position = position
    
object_types = [[((0,32), (0,54), (44,88), (84,88), (84,64), (48,0), (18,0)), 200, 20, 0, 0, 0, 2], [((0,40), (24,0), (36,0),(108,32),(108,48),(0,48)), 200, 20, 0, 0, 0, 2], [2700, 40, 0, 0, 0, 0, 2, 1], #player, player ducking and ground
                [140,80,1280,60], [40, 80,1280,60], [40, 40,1280,40], [80, 40,1280,40], [120, 40,1280,40], #cactuses
                [80, 40, 1280, 40], [80, 40, 1280, 89], [80, 40, 1280, 129]] #birds
sprite_types = [[[pyg.image.load("sprites/dino/kostium3.png"), pyg.image.load("sprites/dino/kostium5.png"),pyg.image.load("sprites/dino/kostium3.png"),pyg.image.load("sprites/dino/kostium6.png")], True, (200, 60)],
                [pyg.image.load("sprites/dino/kostium3.png"), False, (200, 60)],
                [[pyg.image.load("sprites/dino/kostium0.png"), pyg.image.load("sprites/dino/kostium1.png"),pyg.image.load("sprites/dino/kostium0.png"),pyg.image.load("sprites/dino/kostium2.png")], True, (200, 60)],
                [pyg.image.load("sprites/dino/kostium4.png"), False, (200, 60)]]
font.add_file('PressStart2P.ttf')
PressStart2P = font.load('Press Start 2P')

if os.stat('highscore.txt').st_size == 0:
    with open('highscore.txt', 'w') as f:
        f.write(str(0))

class Window(pyg.window.Window):
    def __init__(self, *args, **kwargs): #arguments and keyword arguments
        super().__init__(*args, **kwargs)
        pyg.gl.glClearColor(1000,1000,1000,1000) #background colour
        self.set_location(30, 50) #window position
        self.fps = FPSDisplay(self)

        self.space = pym.Space() #pymunk space
        self.options = DrawOptions() #pymunk + pyglet integration

        self.player = Player_Object(self.space, *object_types[0])
        self.ground = Game_Object(self.space, *object_types[2])
        self.enemy_list = []

        self.player_sprite_walking = Sprites(*sprite_types[0])
        self.player_sprite_jumping = Sprites(*sprite_types[1])
        self.player_sprite_ducking = Sprites(*sprite_types[2])
        self.player_sprite_dead = Sprites(*sprite_types[3])

        self.sleep = 30 #30 frames untill first enemy
        self.randomsleep_down = 90
        self.randomsleep_up = 150
        self.state = None #the players state
        self.running = True

        ground_handler = self.space.add_collision_handler(1, 2) #collision handler to know when player is on the ground
        ground_handler.begin = self.coll_ground

        end_handler = self.space.add_collision_handler(2, 3)
        end_handler.begin = self.coll_enemy
        
        self.counter_vel = 2
        self.enemy_velocity = -250

        self.points = 0
        self.scoreLabel = pyg.text.Label('',
                                 font_name='Press Start 2P',
                                 font_size=20,
                                 color=(83, 83, 83, 255),
                                 x=1180, y=700,
                                 anchor_x='center', anchor_y='center')
        self.highscoreLabel = pyg.text.Label('HI',
                                 font_name='Press Start 2P',
                                 font_size=20,
                                 color=(115, 115, 115, 255),
                                 x=980, y=700,
                                 anchor_x='center', anchor_y='center')
        self.counter_score = 0.1
        self.value_holder = 0.1
        self.speedup_score = 3
        self.highscore = self.load()


    def on_draw(self):
        self.clear()
        self.space.debug_draw(self.options) #drawing the pymunk space in pyglet
        self.fps.draw()
        self.sprite_update()
        self.scoreLabel.draw()
        self.highscoreLabel.draw()

    def on_key_press(self, symbol, modifiers):
        if self.state == None:
            if symbol == key.SPACE or symbol == key.UP:
                self.jumping_time = 0
                self.state = 'jumping'
            elif symbol == key.DOWN: 
                self.state = 'ducking'


    def on_key_release(self, symbol, modifiers):
        if symbol == key.SPACE or symbol == key.UP and self.state == 'jumping':
            self.state = 'falling'
        elif symbol == key.DOWN and self.state == 'ducking':
            self.state = 'unducking'

    def coll_ground(self, arbiter, space, data):
        if self.state != 'ducking' and self.state != 'unducking': #ducking is done on the ground
            self.state = None
        return True

    def coll_enemy(self, arbiter, space, data):
        self.running = False
        return False

    def update(self, dt): #date and time
        if self.running:
            self.space.step(dt) #steps every frame
            self.action(self.player, self.state)
            self.enemy_generation()
            self.enemy_removal()
            self.speed_up(dt)
            if self.points < 99999:
                self.score(dt)
            self.scoreLabel.text = f'{self.points}'
            self.highscoreLabel.text = f'HI {self.highscore}'
        else:
            if self.highscore < self.points:
                self.modify_highscore(self.points)

    def action (self, player, state=None):
        if self.state == 'jumping':
            self.jumping_time += 1
            if self.jumping_time == 1:
                player.velocity += 0, 280
            elif self.jumping_time == 7: #allows you to jump for only x iterations of the update class
                self.state = 'falling'
            player.velocity += 0, 35 #this and falling, define our space gravity
        elif self.state == 'falling':
            player.velocity += 0, -20 #see above
        elif self.state == 'ducking':
            self.space.remove(self.player.shape) #deletes the player, to then create a smaller one
            self.player = Player_Object(self.space, *object_types[1])
        elif self.state == 'unducking':
            self.space.remove(self.player.shape) #deletes small player and creates a new, normally sized one
            self.player = Player_Object(self.space, *object_types[0])
            self.state = None #changes the state because ducking is on the ground, see coll_ground class
        else:
            player.velocity = 0, 0 #None means on the player is on the ground

    def enemy_generation(self):
        self.sleep -= 1
        if self.sleep == 0:
            self.sleep = random.randint(self.randomsleep_down, self.randomsleep_up) #random sleep time intil new enemy is generated
            x = random.randint(3,10)
            self.enemy_list.append(Game_Object(self.space, *object_types[x], self.enemy_velocity, 0, 1, 3))

    def enemy_removal(self):
        for index, enemy in enumerate(self.enemy_list):
            if enemy.position[0] < -50:
                self.space.remove(enemy, enemy.shape)
                self.enemy_list.pop(index)

    def sprite_update(self): #to do
        if not self.running :
            self.player_sprite_dead.position = (self.player.position[0], self.player.position[1])
            self.player_sprite_dead.draw()
        elif self.state == "jumping" or self.state == "falling" :
            self.player_sprite_jumping.position = (self.player.position[0], self.player.position[1])
            self.player_sprite_jumping.draw()
        elif self.state == "ducking" :
            self.player_sprite_ducking.position = (self.player.position[0], self.player.position[1])
            self.player_sprite_ducking.draw()
        else:
            self.player_sprite_walking.position =(self.player.position[0], self.player.position[1])#self.player.position
            self.player_sprite_walking.draw()

    def speed_up(self, dt):
        self.counter_vel -= dt
        if self.counter_vel < 0:
            self.enemy_velocity -= 10
            self.counter_vel = 2
            if self.randomsleep_up > 60:
                self.randomsleep_up -= 2
            if self.randomsleep_down > 20:
                self.randomsleep_down -= 2

    def score(self, dt):
        self.counter_score -= dt
        if self.counter_score <0:
            self.points += 1
            self.speedup_score -= dt
            self.counter_score = self.value_holder
        if self.speedup_score <0:
            self.counter_score = self.value_holder - 0.5 * dt
            self.value_holder = self.counter_score
            self.speedup_score = 3

    def modify_highscore(self, score):
        open('highscore.txt', 'w').close()
        with open('highscore.txt', 'w') as f:
            f.write(str(score))

    def load(self):
        with open('highscore.txt') as f:
            score = int(f.read())
        return score

window = Window(1280, 720, 'Pymunk', resizable=False)
pyg.clock.schedule_interval(window.update, 1/60) #60 frames per second
pyg.app.run()