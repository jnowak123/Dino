import pyglet as pyg
from pyglet.window import FPSDisplay, key

class Game_Object():
    def __init__(self, posx, posy, image=None):
        self.posx = posx
        self.posy = posy
        self.vel = 0
        if image is not None:
            image = pyg.image.load('sprites/' + image)
            self.sprite = pyg.sprite.Sprite(image, x=self.posx, y=self.posy)

    def draw(self):
        self.sprite.draw()

    def update(self, dt):
        self.sprite.y += self.vel*dt
        self.sprite.y -= 3

class Shape():
    def __init__(self):
        self.shape = pyg.shapes.Rectangle(0, 0, 2000, 40)
    
class Window(pyg.window.Window):
    def __init__(self, *args, **kwargs): #arguments and keyword arguments
        super().__init__(*args, **kwargs)
        self.set_location(30, 50) #window position
        self.framerate = 1/60
        self.fps = FPSDisplay(self)

        self.player = Game_Object(200, 40, 'dino1.png')
        self.ground = Shape()
        self.enemy_types = [(200,200,200,200)]

    def on_draw(self):
        self.clear()
        self.player.draw()
        self.ground.shape.draw()

    def on_key_press(self, symbol, modifiers):
        if symbol == key.SPACE or symbol == key.UP:
            self.player.vel += 1000

    def on_key_release(self, symbol, modifiers):
        if symbol == key.SPACE or symbol == key.UP:
            self.player.vel = 0

    def update(self, dt):
        self.player.update(dt)

window = Window(1280, 720, 'Dino', resizable=False)
pyg.clock.schedule_interval(window.update, window.framerate) #60 frames per second
pyg.app.run()