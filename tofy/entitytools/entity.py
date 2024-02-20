import pyglet
from pyglet.gl import GL_ONE_MINUS_SRC_ALPHA, GL_SRC_ALPHA



#the main observer class
class Entity(pyglet.sprite.Sprite, pyglet.event.EventDispatcher):
    def __init__(self, img, x, y, z, batch, group):
        super().__init__(img, x, y, z, batch = batch, group=group)
        #list of subjects to listen to
        self.subjects = []
    def listen_to_subject(self, subject):
        self.subjects.append(subject)
        subject.push_handlers(self)  
    def stop_listening_to_subject(self, subject):
        self.subjects.remove(subject)
        subject.remove_handler(self)
    def create_new_topic(self, topic_name:str):
        self.register_event_type(topic_name)
    #deleting the entity will need to not only remove it's initilized class, but also to remove it from every subject, which means, me need to use an event system to say so to everyone
    def delete(self):
        for subject in self.subjects:
            self.StopListeningToSubject(subject)
        del self
    def behaviour():
        pass
    