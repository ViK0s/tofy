import pyglet


import sys
sys.path.append("/Users/PC/Desktop/anduril/")

import eugor

lol = eugor.entitytools.entity.Entity

class GameWindow(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.active = 1
    def on_draw(self):
        self.render()
    def render(self):
        self.clear()

        self.pre_render()

        playerobject.draw()
        enemie1s.draw()
        self.flip()

    def run(self):
        while self.active == 1:
            self.render()

            # -----------> This is key <----------
            # This is what replaces pyglet.app.run()
            # but is required for the GUI to not freeze
            #
            event = self.dispatch_events()
            self.push_handlers(playerobject.key_handler)
    def pre_render(self):
        pass  
    def on_close(self):
        pyglet.app.exit()
        self.active = 0
        self.close()






class Snake(eugor.entitytools.entity.Enemy):
    def __init__(self, subject, *args, **kwargs):
        super().__init__(subject, *args, **kwargs)
    def turn_end(self):
        print("the enemy is ending turn tooo!!!!!!")
        self.x += 5

x = GameWindow()


pic = pyglet.image.load('C:/Users/PC/Desktop/anduril/examples/esas.png')




playerobject = eugor.entitytools.player.Player(x, pic, 100, 100)
enemie1s = Snake(playerobject, pic, 0, 0)

x.run()

