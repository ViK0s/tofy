import entitytools
import pyglet
from pyglet.window import key

#this should probably be merged to entity.py but i'll leave this for now
# pretty much the player class is an observer but also a subject
#player is observing for the input, and enemies (attacking)
#enemies are observing for end turn and the player (attacking)
class Player(entitytools.entity.Entity, pyglet.event.EventDispatcher):
    def __init__(self, window, *args, **kwargs):
        super().__init__(*args, **kwargs)


        window.push_handlers(self.on_key_press)
        self.key_handler = key.KeyStateHandler()
        self.event_handlers = [self, self.key_handler]

        self.register_event_type('turn_end')
    # this should check a list becaus sometimes we want to change our controls  
    def on_key_press(self, symbol, modifiers):
        if symbol == key.SPACE:
            print("bruh")
            self.dispatch_event('turn_end')
    def turn_end(self):
        print("im ending turn bruh")
        