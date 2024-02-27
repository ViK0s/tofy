import tofy
import pyglet


class World():
    def __init__(self, tilesetlist, player, entitylist):
        self.tilesetlist = tilesetlist
        self.player = player
        self.entitylist = entitylist
        
    def checkFOV(self):
        #the number on tilesetlist should be the current tileset
        for i in self.tilesetlist[0].tilelist:
            #if i[self.player.relativex].y == self.player.y:
            i[self.player.relativex + 1].batch = self.tilesetlist[0].batch
            i[self.player.relativex + 2].batch = self.tilesetlist[0].batch
            i[self.player.relativex + 3].batch = self.tilesetlist[0].batch
            i[self.player.relativex + 4].batch = self.tilesetlist[0].batch
            #for n in i:
            #    if n.x < self.player.x and n.y == self.player.y:
            #        print("im here")
            #        n.batch = self.tilesetlist[0].batch