import tofy
import pyglet


class World():
    def __init__(self, tilesetlist, player, entitylist):
        self.tilesetlist = tilesetlist
        self.player = player
        self.entitylist = entitylist