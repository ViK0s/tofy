import eugor
import pyglet


#this sohuld also be merged into entity.py probably!
class Enemy(eugor.entitytools.entity.Entity):
    def __init__(self, subject, *args, **kwargs):
        super().__init__(*args, **kwargs)
        subject.push_handlers(self)
    #basic behaviour of enemy on their turn!
    def behaviour():
        pass