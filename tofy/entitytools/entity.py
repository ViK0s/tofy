import pyglet
from pyglet.gl import GL_ONE_MINUS_SRC_ALPHA, GL_SRC_ALPHA



#the main observer class
class Entity(pyglet.sprite.Sprite, pyglet.event.EventDispatcher):
    def __init__(self, img, relativex, relativey, z, batch, group, tileset):
        x = tileset.x + relativex*(tileset.tilemap.tile_width+tileset.tilespace[0])
        y = tileset.y + relativey*(tileset.tilemap.tile_height+tileset.tilespace[1]) 
        super().__init__(img, x, y, z, batch = batch, group = group)
        self.tileset = tileset
        
        self._relativex = relativex
        self._relativey = relativey
    
        self.relativepos = (relativex, relativey)
        #list of subjects to listen to
        self.subjects = []
    
        
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
        self.subjects.append(subject)
        subject.push_handlers(self)  
    def stop_listening_to_subject(self, subject):
        self.subjects.remove(subject)
        subject.remove_handler(self)
    def create_new_topic(self, topic_name:str):
        self.register_event_type(topic_name)
    #deleting the entity will need to not only remove it's initilized class, but also to remove it from every subject, which means, we need to use an event system to say so to everyone
    def delete(self):
        for subject in self.subjects:
            self.StopListeningToSubject(subject)
        del self
    def behaviour():
        pass
    