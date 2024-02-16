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

        #playerbatch.draw()

        self.flip()

    def run(self):
        while self.active == 1:
            self.render()

            # -----------> This is key <----------
            # This is what replaces pyglet.app.run()
            # but is required for the GUI to not freeze
            #
            event = self.dispatch_events()
    def pre_render(self):
        pass  
    def on_close(self):
        pyglet.app.exit()
        self.active = 0
        self.close()



x = GameWindow()

x.run()