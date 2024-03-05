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
    def __init__(self, x, y, height, width, tilemap, batch, group, tilespace:list):
        
        #height and width of the tileset
        self.height = height
        self.width = width
        
        #tilemap
        self.tilemap = tilemap
        
        #check if the tilemap was properly initialized, if not, raise an error
        if self.tilemap.tilemap == []:
            raise _TilemapNotInitialized
        
        #this is the true tilelist - all the tiles have real relative positions
        self.tilelist = []
        
        #list of tiles that should be drawn now, allows implementation of FOV
        self.tilestodraw = []
        
        #bottom left corner 
        self.x = x
        self.y = y
        
        #batch and group
        self.batch = batch
        self.group = group

        #the amount of space between tiles, in px
        self.tilespace = tilespace
        
        #list of visible tiles
        self.visible = []

        #list of collidables
        self.collidabletiles = []

        #find the corners of the tileset so it's easier to manipulate it's position
        #starting from downward left, going counterclockwise
        self.x1 = self.x
        self.y1 = self.y

        self.x2 = self.x + (self.width * (self.tilemap.tile_width+self.tilespace[0]))
        self.y2 = self.y

        self.y3 = self.y + (self.height * (self.tilemap.tile_height+self.tilespace[1]))
    
    def createsquare(self, tileimgx:int, tileimgy:int):
        tempy = []
        
        for i in range(0, self.height):
            for n in range(0, self.width):
                #this looks pretty digusting and is not up to standards of PEP 8, but it works #pxwidth
                tempy.append(Tile(self.tilemap.tilemap[tileimgy][tileimgx],self.x + (n*(self.tilemap.tile_width+self.tilespace[0])), self.y + (i*(self.tilemap.tile_height+self.tilespace[1])), 0.1, None, self.group, False, n, i))
                
            self.tilelist.append(tempy)
            tempy = []
    #useful for making a list of collidables
    def aggregate_collidables(self):
        for ytiles in self.tilelist:
            for xtile in ytiles:
                if xtile.collidable: 
                    self.collidabletiles.append(xtile)
    def dbcreate():
        pass

    