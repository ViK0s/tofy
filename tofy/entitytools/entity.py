"""Base module containing classes representing objects in the game world"""


import pyglet
from pyglet.gl import GL_ONE_MINUS_SRC_ALPHA, GL_SRC_ALPHA
from tofy.tiletools.tileset import *


#the main observer class
class Entity(pyglet.sprite.Sprite, pyglet.event.EventDispatcher):
    """Base class upon which every object expands on"""
    def __init__(self, img, relativex, relativey, z, batch, group, tileset):
        #calculate the real position
        x = tileset.x + relativex*(tileset.tilemap.tile_width+tileset.tilespace[0])
        y = tileset.y + relativey*(tileset.tilemap.tile_height+tileset.tilespace[1]) 
        super().__init__(img, x, y, z, batch = batch, group = group)
        
        self.tileset = tileset
        
        self._relativex = relativex
        self._relativey = relativey
    
        #self.relativepos = (relativex, relativey)
        #list of subjects to listen to
        self.subjects = []
    
        self.tilesetloc = 0
    @property
    def relativex(self):
        return self._relativex
        
    
    @relativex.setter
    def relativex(self, relativex):
        self._relativex = relativex
        self.x = self.tileset.x + self.relativex*(self.tileset.tilemap.tile_width+self.tileset.tilespace[0])

    @property
    def relativey(self):
        return self._relativey
        
    
    @relativey.setter
    def relativey(self, relativey):
        self._relativey = relativey
        self.y = self.tileset.y + self.relativey*(self.tileset.tilemap.tile_height+self.tileset.tilespace[1])



    def listen_to_subject(self, subject):
        """Listen to a specific object for events"""
        self.subjects.append(subject)
        subject.push_handlers(self)  
    def stop_listening_to_subject(self, subject):
        """Stop listening to a specific object for events"""
        self.subjects.remove(subject)
        subject.remove_handler(self)
    def create_new_topic(self, topic_name:str):
        """Create a new event type"""
        self.register_event_type(topic_name)


    def settileset(self, tilesetloc, newtileset:Tileset, newposx, newposy):
        """Set a new tileset and location on it"""
        self.tilesetloc = tilesetloc
        self.tileset = newtileset
        self.relativex = newposx
        self.relativey = newposy
        #push events to the new tileset
        self.push_handlers(newtileset)


class Enemy(Entity):
    """Base class for enemies"""
    def __init__(self, img, relativex, relativey, z, batch, group, tileset, attributes:dict):
        super().__init__(img, relativex, relativey, z, batch, group, tileset)
        self.attributes = attributes
        #unused, when spawning enemies there was supposed to be a "risk limit", every would then have a risk attribute
        #which would have been used to calculate the total risk
        #self.risk = self.calculaterisk()
        self.hp = attributes["hp"]
    def on_attack(self, dmg, atkent, s ,d):
        """handle the on_attack event"""
        #sent by entitytools.player class
        self.checkhp()

    """def calculaterisk(self):
        risk = (self.attributes["dmg"] * 5) + (self.attributes["speed"] * 2) + (len(self.attributes["special"]) * 20)
        return risk"""
    
    def detectcollisionwithplayer(self, i, relativechangex, relativechangey):
        if i.relativex == self.relativex + relativechangex and i.relativey == self.relativey + relativechangey:
            self.dispatch_event("attack", self.attributes["dmg"], self.attributes["name"])
            return True
    def checkhp(self):
        """Despawn the enemy if it's hp == 0"""
        if self.attributes["hp"] <= 0:
            self.batch = None

class Item(Entity):
    """Base class for items"""
    def __init__(self, img, relativex, relativey, z, batch, group, tileset, attributes:dict):
        super().__init__(img, relativex, relativey, z, batch, group, tileset)
        self.attributes = attributes
        self.hp = attributes["hp"]


    def calculateworth(self):
        pass