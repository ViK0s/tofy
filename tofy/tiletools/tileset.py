import tile
import pyglet
# this is something like a "game world"
# this should have support for tiled, own tools could be a good idea too

class Tileset:
    def __init__(self, x, y, height, width, tilemap, batch, group):
        self.height = height
        self.width = width
        self.tilemap = tilemap
        self.tilelist = []
        self.x = x
        self.y = y
        self.batch = batch
        self.group = group
    def createrectangle(self):
        for i in range(0, self.height):
            for n in range(0, self.width):
                self.tilelist.append(tile.Tile(self.tilemap.tilemap[1], self.x + (n*20), self.y + (i*20), 0.1, self.batch, self.group, False))

    def dbcreate():
        pass