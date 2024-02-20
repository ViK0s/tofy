import pyglet


import sys
sys.path.append("/Users/PC/Desktop/anduril/")

import tofy

lol = tofy.entitytools.entity.Entity

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






class Snake(tofy.entitytools.entity.Entity):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    def on_attack(self):
        print("the enemy is getting attacked")



class GamePlayer(tofy.entitytools.player.Player):
    def __init__(self, window, img, x, y, z, batch, group):
        super().__init__(window, img, x, y, z, batch, group)
    def on_key_press(self, symbol, modifiers):
        if symbol == self.key.SPACE:
            print("im tha playa")
            self.dispatch_event("on_attack")

x = GameWindow()


pic = pyglet.image.load('C:/Users/PC/Desktop/anduril/examples/esas.png')




playerobject = GamePlayer(x, pic, 100, 100, 0.1, None, None)
playerobject.CreateNewTopic("on_attack")

enemie1s = Snake(pic, 0, 0, 0.1, None, None)
enemie1s.ListenToSubject(playerobject)

x.run()

