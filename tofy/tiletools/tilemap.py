import tile
import pyglet

#this class should be compatible with Tiled, and also it would be nice to create a method to make fonts into tilesets

# this should pretty much be class contatining all the tile data, this is not the same as tileset!
# tilemap contains just how a tile looks, tileset says where those tiles are in the world etc.

class Tilemap:
    def __init__(self):
        self.tilemap = []
    def create_from_img(self, img, rows, columns):
        temp = pyglet.image.ImageGrid(img, rows, columns)
        
        #read how big a single tile is, so that tilesets can easily use that info
        self.tile_height = temp.item_height
        self.tile_width = temp.item_width
        
        self.tilemap = [temp[i:i+rows] for i in range(0, len(temp), rows)]
    def changecolouring():
        pass
    def dbcreate():
        pass