import tile
import pyglet
# this is something like a "game world"


class Tileset:
    def __init__(self, height, width, tilemap):
        self.height = height
        self.width = width
        self.tilemap = tilemap
    def createrectangle(self):
        tilelist = []
        for i in range(0, self.height):
            for n in range(0, self.width):
                tilelist.append(tile.Tile(self.tilemap.tilemap, self.x + (n*20), self.y + (i*20), 0.1, self.batch, self.group))
        self.tilelist = tilelist
    def dbcreate():
        pass