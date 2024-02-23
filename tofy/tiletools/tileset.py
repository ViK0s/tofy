from tofy.tiletools.tile import Tile
import sys
import pyglet
# this is something like a "game world"
# this should have support for tiled, own tools could be a good idea too

class _TilemapNotInitialized(Exception):
    def __init__(self):
        self.message = "Exception occured: passed tilemap was not initialized"
        super().__init__(self.message)



class Tileset:
    def __init__(self, x, y, height, width, tilemap, batch, group, tilespace):
        
        #height and width of the tileset
        self.height = height
        self.width = width
        
        self.tilemap = tilemap
        #check if the tilemap was properly initialized, if not, raise an error
        if self.tilemap.tilemap == []:
            raise _TilemapNotInitialized
        
       
        self.tilelist = [[0]*height]*width
        
        #bottom left corner 
        self.x = x
        self.y = y
        
        #batch and group
        self.batch = batch
        self.group = group

        #the amount of space between tiles, in px
        self.tilespace = tilespace
    def createrectangle(self, tileimgx:int, tileimgy:int):
        for i in range(0, self.width):
            for n in range(0, self.height):
                #this looks pretty digusting and is not up to standards of PEP 8, but it works
                self.tilelist[i].append(Tile(self.tilemap.tilemap[tileimgy][tileimgx],self.x + (i*(self.tilemap.tile_width+self.tilespace)), self.y + (n*(self.tilemap.tile_height+self.tilespace)), 0.1, self.batch, self.group, False))
        

    def dbcreate():
        pass