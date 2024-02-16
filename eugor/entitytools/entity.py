import pyglet



#the main observer class
class Entity(pyglet.sprite.Sprite):
    def __init__(self, subject,*args, **kwargs):
        super(Entity, self).__init__(*args, **kwargs)
        subject.push_handlers(self)
    def addSubject():
        pass
    