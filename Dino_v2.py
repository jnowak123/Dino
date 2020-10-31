import pyglet as pyg
from pyglet.window import FPSDisplay, key

class Game_Object():
    def __init__(self, posx, posy, image=None):
        self.posx = posx
        self.posy = posy
        self.vely = 0
        self.velx = 0
        if image is not None:
            image = pyg.image.load('sprites/' + image)
            self.sprite = pyg.sprite.Sprite(image, x=self.posx, y=self.posy)

    def draw(self):
        self.sprite.draw()

    def update(self, dt):
        self.sprite.y += self.vely*dt
        self.sprite.x += self.velx*dt

class Window(pyg.window.Window):
    def __init__(self, *args, **kwargs): #arguments and keyword arguments
        super().__init__(*args, **kwargs)
        self.set_location(30, 50) #window position
        self.framerate = 1/60
        self.fps = FPSDisplay(self)

        self.player = Game_Object(200, 40, 'dino.png')
        self.player2 = Game_Object(500, 40, 'dino.png')

    def on_draw(self):
        self.clear()
        self.player.draw()
        self.player2.draw()

    def on_key_press(self, symbol, modifiers):
        if symbol == key.SPACE or symbol == key.UP:
            self.player.vely += 10
        if symbol == key.RIGHT:
            self.player.velx += 50

    def on_key_release(self, symbol, modifiers):
        if symbol == key.SPACE or symbol == key.UP:
            self.player.vely = 0
        if symbol == key.RIGHT:
            self.player.velx = 0

    def update(self, dt):
        self.player.update(dt)
        self.player2.update(dt)

window = Window(1280, 720, 'Dino', resizable=False)
pyg.clock.schedule_interval(window.update, window.framerate) #60 frames per second
pyg.app.run()