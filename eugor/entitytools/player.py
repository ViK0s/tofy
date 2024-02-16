import entitytools
import pyglet
from pyglet.window import key

#this should probably be merged to entity.py but i'll leave this for now
class Player(entitytools.entity.Entity):
    def __init__(self):
        self.key_handler = key.KeyStateHandler()
        self.event_handlers = [self, self.key_handler]

    def on_key_press(self, symbol, modifiers):
        if symbol == key.SPACE:
            print("essa")
    def on_end_turn():
        pass