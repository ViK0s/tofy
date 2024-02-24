import entitytools
import pyglet
from pyglet.window import key

#this should probably be merged to entity.py but i'll leave this for now
# pretty much the player class is an observer but also a subject
#player is observing for the input, and enemies (attacking)
#enemies are observing for end turn and the player (attacking)
class Player(entitytools.entity.Entity):
    def __init__(self, window, img, relativex, relativey, z, batch, group, tileset):
        super().__init__(img, relativex, relativey, z, batch, group, tileset)
        
        self.tileset = tileset


        self.key_handler = key.KeyStateHandler()
        self.key = key
        window.push_handlers(self.on_key_press)
        #self.event_handlers = [self, self.key_handler]

        
    # this is the default method for handling player controls
    # this should be overwritten when creating a new game!
    def on_key_press(self, symbol, modifiers):
        pass
    
    def detect_collision(self, relativechangex, relativechangey):
        if self.tileset.tilelist[self.relativey + relativechangey][self.relativex + relativechangex].collidable == True: return True 

        