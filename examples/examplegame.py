import pyglet


import sys
sys.path.append("/Users/micha/Desktop/tofy-main/")

import tofy



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
        #enemie1s.draw()
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
            #self.push_handlers(playerobject.key_handler)
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
    def __init__(self, window, img, relativex, relativey, z, batch, group, tileset):
        super().__init__(window, img, relativex, relativey, z, batch, group, tileset)
    def on_key_press(self, symbol, modifiers):
        if symbol == self.key.RIGHT and not self.detect_collision(1, 0, worldobject):
            print("im tha playa")
            #self.dispatch_event("on_attack")
            self.relativex += 1
            #print(self.x)
            worldobject.checkFOV()
        if symbol == self.key.LEFT and not self.detect_collision(-1, 0, worldobject):
            self.relativex -= 1
            worldobject.checkFOV()
        if symbol == self.key.UP and not self.detect_collision(0, 1, worldobject):
            self.relativey += 1
            worldobject.checkFOV()
        if symbol == self.key.DOWN and not self.detect_collision(0, -1, worldobject):
            self.relativey -= 1
            worldobject.checkFOV()

x = GameWindow()


tileimages = pyglet.resource.image("curses_800x600.png")



tilemap = tofy.tiletools.tilemap.Tilemap()
tilemap.create_from_img(tileimages, 16, 16)

#print(tilemap.tile_height, tilemap.tile_width)
foreground = pyglet.graphics.Group(order=1)
background = pyglet.graphics.Group(order=0)
batch = pyglet.graphics.Batch()

#testcollisiontile = tofy.tiletools.tile.Tile(tilemap.tilemap[5][5], 40, 40, 0.1, batch, foreground, True)


tilesetdef = tofy.tiletools.tileset.Tileset(20, 20, 20, 20, tilemap, batch, background, [4, 10])
esa = tilesetdef.createsquare(2, 2)


playerobject = GamePlayer(x, tilemap.tilemap[15][1], 10, 10, 0.1, batch, foreground, tilesetdef)
playerobject.create_new_topic("on_attack")



tilesetdef.tilelist[11][11].collidable = True
tilesetdef.tilelist[11][10].collidable = True
tilesetdef.tilelist[11][9].collidable = True
#testing lower fov
tilesetdef.tilelist[9][10].collidable = True
tilesetdef.tilelist[9][9].collidable = True
tilesetdef.tilelist[9][11].collidable = True
#enemie1s = Snake(tilemap.tilemap[1][1], 3, 0, 0.1, batch, foreground, tilesetdef)
#enemie1s.listen_to_subject(playerobject)

worldobject = tofy.world.World([tilesetdef], playerobject, [])
worldobject.checkFOV()
#print(worldobject.LineOfSight(1, 1, 3, 4))

x.run()

