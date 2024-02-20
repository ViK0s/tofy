import pyglet


import sys
sys.path.append("/Users/PC/Desktop/tofy-main/")

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
        batch.draw()
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


tileimages = pyglet.resource.image("curses_800x600.png")


tilemap = tofy.tiletools.tilemap.Tilemap()
tilemap.create_from_img(tileimages, 16, 16)

batch = pyglet.graphics.Batch()

tileset = tofy.tiletools.tileset.Tileset(200, 200, 10, 10, tilemap, batch, None)
tileset.createrectangle()


playerobject = GamePlayer(x, tilemap.tilemap[0], 100, 100, 0.1, None, None)
playerobject.create_new_topic("on_attack")

enemie1s = Snake(tilemap.tilemap[1], 0, 0, 0.1, None, None)
enemie1s.listen_to_subject(playerobject)

x.run()

