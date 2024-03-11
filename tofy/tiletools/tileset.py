from tofy.tiletools.tile import Tile
import sys
import pyglet
import opensimplex
# this is something like a "game world"
# this should have support for tiled, own tools could be a good idea too

class _TilemapNotInitialized(Exception):
    def __init__(self):
        self.message = "Exception occured: passed tilemap was not initialized"
        super().__init__(self.message)



class Tileset():
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
        self.noncollidabletiles = []

        #find the corners of the tileset so it's easier to manipulate it's position
        #starting from downward left, going counterclockwise
        self.x1 = self.x
        self.y1 = self.y

        self.x2 = self.x + ((self.width-1) * (self.tilemap.tile_width+self.tilespace[0]))-self.tilespace[0]
        self.y2 = self.y

        self.y3 = self.y + ((self.height-1) * (self.tilemap.tile_height+self.tilespace[1]))
    
        self.unexplored = True
    def createsquare(self, tileimgx:int, tileimgy:int):
        self.unexplored = False
        tempy = []
        
        for i in range(0, self.height):
            for n in range(0, self.width):
                #this looks pretty digusting and is not up to standards of PEP 8, but it works #pxwidth
                tempy.append(Tile(self.tilemap.tilemap[tileimgy][tileimgx],self.x + (n*(self.tilemap.tile_width+self.tilespace[0])), self.y + (i*(self.tilemap.tile_height+self.tilespace[1])), 0.1, None, self.group, False, n, i))
                
            self.tilelist.append(tempy)
            tempy = []
    #useful for making a list of collidables
    def aggregate_collidables(self):
        self.collidabletiles = []
        for ytiles in self.tilelist:
            for xtile in ytiles:
                if xtile.collidable: 
                    self.collidabletiles.append(xtile)
    
    def aggregate_noncollidable(self):
        self.noncollidabletiles = []
        for ytiles in self.tilelist:
            for xtile in ytiles:
                if not xtile.collidable: 
                    self.noncollidabletiles.append(xtile)
    def dbcreate():
        pass

    def gen_cave(self):
        
        opensimplex.random_seed()

        """xpix = 30
        ypix = 30"""
        scale = 6
        pic = []

        for i in range(self.width):
            row = []
            for j in range(self.height):
                noise_val = 1* opensimplex.noise2(i/scale, j/scale)
                noise_val += 0.5*opensimplex.noise2(i/scale, j/scale)
                noise_val += 0.25*opensimplex.noise2(i/scale, j/scale)
                #noise_val = noise_val / (0.5 + 0.25 + 0.125)
                #noise_val = noise_val ** 0.5
                if noise_val < 0.5:
                    noise_val = 0
                if noise_val > 0.5:
                    noise_val = 1
                
                row.append(noise_val)
            pic.append(row)
        
        
        #print(pic)
        
        
        
        tempy = []
        
        for i in range(0, self.height):
            for n in range(0, self.width):
                #this looks pretty digusting and is not up to standards of PEP 8, but it works #pxwidth
                if pic[i][n] == 1:
                    tempy.append(Tile(self.tilemap.tilemap[4][2],self.x + (n*(self.tilemap.tile_width+self.tilespace[0])), self.y + (i*(self.tilemap.tile_height+self.tilespace[1])), 0.1, None, self.group, True, n, i))
                else:
                    tempy.append(Tile(self.tilemap.tilemap[4][1],self.x + (n*(self.tilemap.tile_width+self.tilespace[0])), self.y + (i*(self.tilemap.tile_height+self.tilespace[1])), 0.1, None, self.group, False, n, i))


            self.tilelist.append(tempy)
            tempy = []
    
    def createsquarefilled(self, tileimgx:int, tileimgy:int):
        self.unexplored = False
        tempy = []
        
        for i in range(0, self.height):
            for n in range(0, self.width):
                #this looks pretty digusting and is not up to standards of PEP 8, but it works #pxwidth
                tempy.append(Tile(self.tilemap.tilemap[tileimgy][tileimgx],self.x + (n*(self.tilemap.tile_width+self.tilespace[0])), self.y + (i*(self.tilemap.tile_height+self.tilespace[1])), 0.1, None, self.group, True, n, i))
                
            self.tilelist.append(tempy)
            tempy = []
    """def mine(self, pos):
        if self.tilelist[pos[0]][pos[1]].hp <= 0:
            self.tilelist[pos[0]][pos[1]].collidable = False
        self.tilelist[pos[0]][pos[1]].hp -= 1"""