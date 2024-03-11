import pyglet
# this should contain all the functions that have to do with single tile look. It can be used to convert tiles to different
# colors etc. it could have to do with collisions maybe? But that is not yet designed
class Tile(pyglet.sprite.Sprite):
    def __init__(self, img, x, y, z, batch, group, collidable:bool, relativex, relativey, visiblebyplayer = False):
        super().__init__(img, x, y, z, batch = batch, group=group)
        self.collidable = collidable
        self.relativepos = (relativex, relativey)
        self._visiblebyplayer = visiblebyplayer
        self.hp = 5
    @property
    def visiblebyplayer(self):
        return self._visiblebyplayer
    
    @visiblebyplayer.setter
    def visiblebyplayer(self, visiblebyplayer):
        #self.visible = visible
        self._visiblebyplayer = visiblebyplayer
        if visiblebyplayer == False:
            self.color = (128,128,128)
        else:
            self.color = (72, 31, 1)
    
    def changecolor(self):
        pass