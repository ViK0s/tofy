import pyglet
import sys
sys.path.append("/Users/PC/Desktop/tofy-main/")
import tofy

tileimages = pyglet.resource.image("curses_800x600.png")

tilemap = tofy.tiletools.tilemap.Tilemap()
tilemap.create_from_img(tileimages, 16, 16)

foreground = pyglet.graphics.Group(order=0)
background = pyglet.graphics.Group(order=1)
batch = pyglet.graphics.Batch()

tilesetdef = tofy.tiletools.tileset.Tileset(20, 20, 10, 10, tilemap, batch, background)

lol = tofy.entitytools.entity.Entity(tilemap.tilemap[0][0], 1, 1, 0.1, None, None, tilesetdef)

print(lol.x)


lol.relativex = 2

print(lol.x)