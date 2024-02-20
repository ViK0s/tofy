import tile
import pyglet
# this should pretty much be class contatining all the tile data, this is not the same as tileset!
# tilemap contains just how a tile looks, tileset says where those tiles are in the world etc.

class Tilemap:
    def __init__(self):
        self.img = None
        self.database = None
    def create_from_img(self, img, rows, columns):
        self.tilemap = pyglet.image.ImageGrid(img, rows, columns)
    def changecolouring():
        pass
    def dbcreate():
        pass