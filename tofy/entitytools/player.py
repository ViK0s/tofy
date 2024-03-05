import entitytools
import pyglet
from pyglet.window import key
import math

#this should probably be merged to entity.py but i'll leave this for now
# pretty much the player class is an observer but also a subject
#player is observing for the input, and enemies (attacking)
#enemies are observing for end turn and the player (attacking)
class Player(entitytools.entity.Entity):
    def __init__(self, window, img, relativex, relativey, z, batch, group, tileset, FOVrange = 10):
        super().__init__(img, relativex, relativey, z, batch, group, tileset)
        

        self.key_handler = key.KeyStateHandler()
        self.key = key
        window.push_handlers(self.on_key_press)
        #self.event_handlers = [self, self.key_handler]
        self.FOVrange = FOVrange
        #on init cast lines in the direction of upper right and lower right corners
        self.update_vectors()


    # this is the default method for handling player controls
    # this should be overwritten when creating a new game!
    def on_key_press(self, symbol, modifiers):
        pass
    #detect if entity or collidable tile is on the tile we want to move to
    #should probably be made for entity class
    def detect_collision(self, relativechangex, relativechangey, world):
        #check if you don't need to change the tileset
        #happens only  when you are moving from one tileset to the next one
        
        #situation where you go to the right tileset
        if self.relativex + relativechangex >= self.tileset.width and self.tilesetloc + 1 <= world.maxtileset:
            if world.tilesetlist[self.tilesetloc + 1].tilelist[self.relativey][0].collidable:
                return True
            self.dispatch_event("on_tileset_change", self.tilesetloc)
            self.settileset(self.tilesetloc + 1, world.tilesetlist[self.tilesetloc + 1], -1, self.relativey)
            
        
        #situation where you go to the left tileset
        if self.relativex + relativechangex < 0 and self.tilesetloc - 1 >= 0:
            if world.tilesetlist[self.tilesetloc - 1].tilelist[self.relativey][self.tileset.width - 1].collidable == True:
                return True
            self.dispatch_event("on_tileset_change", self.tilesetloc)
            self.settileset(self.tilesetloc - 1, world.tilesetlist[self.tilesetloc - 1], self.tileset.width, self.relativey)

        
        #situation where you go to the top tileset
        if self.relativey + relativechangey >= self.tileset.height and self.tilesetloc + 9 <= world.maxtileset:
            if world.tilesetlist[self.tilesetloc + 9].tilelist[0][self.relativex].collidable:
                return True
            self.dispatch_event("on_tileset_change", self.tilesetloc)
            self.settileset(self.tilesetloc + 9, world.tilesetlist[self.tilesetloc + 9], self.relativex, -1)
            
        
        #situation where you go to the bottom tileset
        if self.relativey + relativechangey < 0 and self.tilesetloc - 9 >= 0:
            if world.tilesetlist[self.tilesetloc - 9].tilelist[self.tileset.height - 1][self.relativex].collidable:
                return True
            self.dispatch_event("on_tileset_change", self.tilesetloc)
            self.settileset(self.tilesetloc - 9, world.tilesetlist[self.tilesetloc - 9], self.relativex, self.tileset.height)
            
       
        #check for collisions with tiles
        
        if self.tileset.tilelist[self.relativey + relativechangey][self.relativex + relativechangex].collidable == True: 
            return True 
        


        #check for collisions with entities
        for i in world.entitylist:
            if i.relativex == self.relativex + relativechangex and i.relativey == self.relativey + relativechangey:
                return True
            
    def update_vectors(self):
        self.magnitude3 = math.sqrt((self.tileset.width-self.relativex)**2 + (self.tileset.height-self.relativey)** 2)
        self.magnitude2 = math.sqrt((self.tileset.width-self.relativex)**2 + (self.relativey)** 2)
    
    