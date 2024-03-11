import pyglet

import pathlib

#bruhhs = os.getcwd()

bruhhs = pathlib.Path(__file__).parent.resolve()
"""print(len(str(bruhhs)))
print(str(bruhhs)[:len(str(bruhhs))-8])
temp = ""
for i in str(bruhhs):
    if i == '\' :
        temp += "/"""
        

"""import sys
sys.path.append(str(bruhhs)[:33])
print(str(bruhhs)[:33])"""
import tofy

pyglet.resource.Location()

class GameWindow(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.active = 1
    def on_draw(self):
        self.render()
    def render(self):
        self.clear()

        self.pre_render()
        centeredcam.begin()
        #playerobject.draw()
        #enemie1s.draw()
        batch.draw()
        #self.flip()
        centeredcam.end()

        

    def run(self):
        while self.active == 1:
            self.render()

            # -----------> This is key <----------
            # This is what replaces pyglet.app.run()
            # but is required for the GUI to not freeze
            #
            event = self.dispatch_events()
            #self.push_handlers(playerobject.key_handler)
    def pre_render(self):
        pass  
    def on_close(self):
        pyglet.app.exit()
        self.active = 0
        self.close()
    


"""
atr = {
dmg
speed
fov
special
}
"""




class GamePlayer(tofy.entitytools.player.Player):
    def __init__(self, window, img, relativex, relativey, z, batch, group, tileset, atr):
        super().__init__(window, img, relativex, relativey, z, batch, group, tileset, atr)
    def attack(self, dmg, name):
        self.atr["hp"] -= dmg
        gamegui.text.text += "\nYou have been attacked by " + name + " for " + str(dmg) + " dmg"
    def checkhp(self):
        if self.atr["hp"] <= 0:
            self.batch = None
            loselabel = pyglet.text.Label("You lose",
                          font_name='Times New Roman',
                          font_size=32,
                          x=self.x, y=self.y,
                          anchor_x='center', anchor_y='center', batch=guibatch, group=guigroup)
            def callback(lol):
                pyglet.app.exit()
                x.active = 0
                x.close()
            pyglet.clock.schedule_interval(callback, 3)
        elif self.atr["hp"] > self.atr["maxhp"]:
            self.atr["hp"] =  self.atr["maxhp"]
            gamegui.Update()
    def checkhunger(self):
        gamegui.elementdict["hungrylabel"].text = " "
        if self.atr["hunger"] <= 0:
            self.atr["hp"] -= 1
            gamegui.elementdict["hungrylabel"].text = "Hungry!"
            gamegui.elementdict["hungrylabel"].color = (205,127,50, 255)
        elif self.atr["hunger"] > self.atr["maxhunger"]:
            self.atr["hunger"] = self.atr["maxhunger"]
    def on_key_press(self, symbol, modifiers):
        if symbol == self.key.RIGHT or self.key.LEFT or self.key.UP or self.key.DOWN:
            self.atr["hunger"] -= 1
            for i in worldobject.entitylist:
                if type(i) == tofy.entitytools.entity.Enemy:
                    i.detectcollisionwithplayer(playerobject, 1, 0)
                    i.detectcollisionwithplayer(playerobject, -1, 0)
                    i.detectcollisionwithplayer(playerobject, 0, 1)
                    i.detectcollisionwithplayer(playerobject, 0, -1)
            gamegui.Update()
            worldobject.enemymovement()
            self.checkhp()
            self.checkhunger()
        if symbol == self.key.RIGHT and not self.detect_collision(1, 0, worldobject):
            temp = playerobject.x
            self.relativex += 1
            dif = abs(playerobject.x - temp)
            self.update_vectors()
            worldobject.checkFOV()
            centeredcam.position = playerobject.x, playerobject.y
            gamegui.x += dif
            
        if symbol == self.key.LEFT and not self.detect_collision(-1, 0, worldobject):
            temp = playerobject.x
            self.relativex -= 1
            dif = -abs(playerobject.x - temp)
            self.update_vectors()
            worldobject.checkFOV()
            centeredcam.position = playerobject.x, playerobject.y
            gamegui.x += dif
            #gamegui.y = playerobject.y
        if symbol == self.key.UP and not self.detect_collision(0, 1, worldobject):
            temp = playerobject.y
            self.relativey += 1
            dif = abs(playerobject.y - temp)
            #print(dif)
            self.update_vectors()
            worldobject.checkFOV()
            centeredcam.position = playerobject.x, playerobject.y
            #print(gamegui.y)
            gamegui.y += dif
            #print(gamegui.y)
        if symbol == self.key.DOWN and not self.detect_collision(0, -1, worldobject):
            temp = playerobject.y
            self.relativey -= 1
            dif = -abs(playerobject.y - temp)
            #print(dif)
            self.update_vectors()
            worldobject.checkFOV()
            centeredcam.position = playerobject.x, playerobject.y
            #print(gamegui.y)
            gamegui.y += dif
            #print(gamegui.y)
        """if symbol == self.key.SPACE:
            print("relative positions: ",self.relativex, self.relativey, self.tilesetloc)
            print("non relative ones: ", self.x, self.y)
            print(worldobject.entitylist)"""
        if symbol == self.key.NUM_1 and playerobject.rootcount > 0:
            playerobject.remove_item("root")
            playerobject.atr["hp"] += 2
            playerobject.atr["hunger"] += 15
            playerobject.count_items()
            gamegui.Update
        """if symbol == self.key.NUM_2 and playerobject.stonecount > 0:
            playerobject.remove_item("stone")
            playerobject.count_items()
            gamegui.Update"""
        if symbol == self.key.NUM_3 and playerobject.potcount > 0:
            playerobject.remove_item("health potion")
            playerobject.atr["hp"] += 50
            playerobject.count_items()
            gamegui.Update
        if symbol == self.key.NUM_4 and gamegui.indx[0]:
            if playerobject.equipped:
                playerobject.equipped = None
                gamegui.elementdict["itemclick"].setstyle(0, len(gamegui.elementdict["itemclick"]), dict(color=(255, 0, 0, 255)))
            else:
                playerobject.equiped = playerobject.inventory[gamegui.indx[0]]
                gamegui.elementdict["itemclick"].setstyle(0, len(gamegui.elementdict["itemclick"]), dict(color=(0, 255, 0, 255)))
x = GameWindow(width = 1024, height = 768, caption="Caverns")




tileimages = pyglet.resource.image("data/curses_800x600.png")



tilemap = tofy.tiletools.tilemap.Tilemap()
tilemap.create_from_img(tileimages, 16, 16)



#print(tilemap.tilemap)
#print(tilemap.tile_height, tilemap.tile_width)
foreground = pyglet.graphics.Group(order=1)
background = pyglet.graphics.Group(order=0)
guigroup = pyglet.graphics.Group(order=2)
higherguigroup = pyglet.graphics.Group(order=3)
batch = pyglet.graphics.Batch()
guibatch = pyglet.graphics.Batch()

#gamegui = GameGUI(0.75*x.width, 0, 0.75*x.width, x.height)
###############################
# Create ingame GUI
###############################
class GameGUI(pyglet.gui.Frame):
    def __init__(self, window, batch, group, x, y, width, height, cell_size=64, order=0 ):
        super().__init__(window, cell_size, order)
        self.batch = batch
        self.group = group
        self.width = width
        self.height = height
        self._x = x
        self._y = y
        
        self.background = pyglet.shapes.BorderedRectangle(x, y, self.width, self.height,border_color = (255, 0, 0, 255),color = (0, 0, 0, 255), batch = self.batch, group = self.group)
        

        self.elementdict = {}

        playerobject.push_handlers(self)

        self.indx = []
    def AddPushButton(self, pos:tuple, imglist, name:str):
        temp = pyglet.gui.PushButton(self.x + pos[0], self.y + pos[1], imglist[0], imglist[1], batch = self.batch, group = self.group)
        temp.set_handler("on_press", self.push_button_handler)
        temp.set_handler("on_release", self.relese_button_handler)
        self.add_widget(temp)
        
        self.elementdict[name] = temp
    def AddFeed(self, width, height, pos, name):
        self.text = pyglet.text.document.FormattedDocument(" ")
        self.text.set_style(0, len(self.text.text), dict(color=(255, 0, 0, 255)))
        temp = pyglet.text.layout.ScrollableTextLayout(self.text, width, height, True, batch= self.batch, group = self.group)
        temp.position = self._x + pos[0], self._y + pos[1], pos[2]
        #temp.anchor_y = "baseline"
        self.elementdict[name] = temp
    def AddToggleButton(self, pos:tuple, imglist, name:str):
        temp = pyglet.gui.ToggleButton(self.x + pos[0], self.y + pos[1], imglist[0], imglist[1], batch = self.batch, group = self.group)
        temp.set_handler("on_toggle", self.push_button_handler)
        self.add_widget(temp)
    @property
    def x(self):
        return self._x
    
    @x.setter
    def x(self, x):
        self._x = x
        self.background.x = x
        for i in self.elementdict:
            if i == "hpcount":
                self.elementdict[i].x = x + 30
            elif i == "dmgcount":
                self.elementdict[i].x = x + 30
            elif i == "hungercount":
                self.elementdict[i].x = x + 30
            elif i == "hungrylabel":
                self.elementdict[i].x = x + 30
            else:
                self.elementdict[i].x = x

    @property
    def y(self):
        return self._y
    
    @y.setter
    def y(self, y):
        self._y = y
        self.background.y = y
        for i in self.elementdict:
            if i == "essa":
                self.elementdict[i].y = y + 500
            elif i == "invroot":
                self.elementdict[i].y = y + 100
            #elif i == "invstone":
            #    self.elementdict[i].y = y + 150
            elif i == "invpot":
                self.elementdict[i].y = y + 130
            elif i == "hpcount":
                self.elementdict[i].y = y + 300
            elif i == "dmgcount":
                self.elementdict[i].y = y + 280
            elif i == "hungercount":
                self.elementdict[i].y = y + 260
            elif i == "hungrylabel":
                self.elementdict[i].y = y + 240
    def push_button_handler(self):
        print("pushed")
    def relese_button_handler(self):
        print("released")
    def mine(self, s, d):
        if len(self.text.text) > 152:
            self.text.text = " "
        self.text.text += "\nYou chip some stone"
    def on_attack(self, dmg, pos, name, type):
        if len(self.text.text) > 152:
            self.text.text = ""
        if type == tofy.entitytools.entity.Item:
            self.text.text += "\nYou pickup " + name
            self.Update()
            if name == "sword":
                self.AddTextLabel((30, 200, 0.1),"itemclick", "Rusty sword")
                buh = playerobject.inventory[-1]
                self.indx.append(playerobject.inventory.index(buh))
        elif type == tofy.entitytools.entity.Enemy:
            self.text.text += "\nYou attack " + name +" for " + str(dmg) + " damage"
    def AddTextLabel(self, pos, name, string):
        temp = pyglet.text.Label(string,
                          font_name='Times New Roman',
                          font_size=12,
                          x=self._x + pos[0], y=self._y + pos[1],
                          anchor_x='left', anchor_y='bottom', batch=self.batch, group=self.group)
        self.elementdict[name] = temp
    def Update(self):
        playerobject.count_items()
        self.elementdict["invroot"].text = "amount of roots: " + str(playerobject.rootcount) + " PRESS NUM1"
        #self.elementdict["invstone"].text = "amount of stones: " + str(playerobject.stonecount)
        self.elementdict["invpot"].text = "amount of health potions: " + str(playerobject.potcount) + " PRESS NUM3"
        self.elementdict["hpcount"].text = "Health: " + str(playerobject.atr["hp"]) + "/" + str(playerobject.atr["maxhp"])
        self.elementdict["dmgcount"].text = "dmg: " + str(playerobject.atr["dmg"])
        self.elementdict["hungercount"].text = "hunger: " + str(playerobject.atr["hunger"]) + "/" + str(playerobject.atr["maxhunger"])

    def out_of_bounds(self):
        if len(self.text.text) > 152:
            self.text.text = ""
        self.text.text += "\nThere's a chasm before you..."
#btnimg = pyglet.resource.image('bsd.png')


#testcollisiontile = tofy.tiletools.tile.Tile(tilemap.tilemap[5][5], 40, 40, 0.1, batch, foreground, True)
centeredcam = tofy.camera.CenteredCamera(x, 20)

guicam = tofy.camera.CenteredCamera(x)

tilesetdef = tofy.tiletools.tileset.Tileset(20, 20, 30, 30, tilemap, None, background, [4, 10])
esa = tilesetdef.createsquarefilled(1, 4)

plratr =  {
"dmg":10,
"speed":1,
"fov":4,
"special":[],
"hp": 100,
"maxhp": 100,
"hunger": 100,
"maxhunger": 100
}


playerobject = GamePlayer(x, tilemap.tilemap[15][1], 10, 10, 0.1, batch, foreground, tilesetdef, plratr)
playerobject.create_new_topic("on_attack")
playerobject.create_new_topic("on_tileset_change")
playerobject.create_new_topic("mine")
playerobject.create_new_topic("out_of_bounds")
playerobject.count_items
"""gamegui = GameGUI(x, batch, guigroup, 420, centeredcam.position[1] - 138, x.width - (0.75 * x.width) + 20, 775)
#gamegui.AddPushButton((200, 200), [tilemap.tilemap[5][6], btnimg], "test_button")
gamegui.AddFeed(200, 200, (0, 500, 0.1), "essa")
gamegui.AddTextLabel((0, 100, 0.1), "invroot", "amount of roots: " + str(playerobject.rootcount))
gamegui.AddTextLabel((0, 150, 0.1), "invstone", "amount of stones: " + str(playerobject.rootcount))
gamegui.AddTextLabel((0, 130, 0.1), "invpot", "amount of health potions: " + str(playerobject.potcount))
gamegui.AddTextLabel((30, 300, 0.1), "hpcount", "Health: " + str(playerobject.atr["hp"]) + "/" + str(playerobject.atr["maxhp"]))
gamegui.AddTextLabel((30, 280, 0.1), "dmgcount", "dmg: " + str(playerobject.atr["dmg"]))
gamegui.AddTextLabel((30, 260, 0.1), "hungercount", "hunger: " + str(playerobject.atr["hunger"]) + "/" + str(playerobject.atr["maxhunger"]))
gamegui.AddTextLabel((30, 240, 0.1), "hungrylabel", " ")
centeredcam.position = playerobject.x, playerobject.y"""

"""tilesetdef.tilelist[11][11].collidable = True
tilesetdef.tilelist[11][10].collidable = True
tilesetdef.tilelist[11][9].collidable = True

tilesetdef.tilelist[11][11].image = tilemap.tilemap[3][3]
tilesetdef.tilelist[11][10].image = tilemap.tilemap[3][3]
tilesetdef.tilelist[11][9].image = tilemap.tilemap[3][3]

#testing lower fov
tilesetdef.tilelist[9][10].collidable = True
tilesetdef.tilelist[9][9].collidable = True
tilesetdef.tilelist[9][11].collidable = True


tilesetdef.tilelist[9][10].image = tilemap.tilemap[3][3]
tilesetdef.tilelist[9][9].image = tilemap.tilemap[3][3]
tilesetdef.tilelist[9][11].image = tilemap.tilemap[3][3]


tilesetdef.tilelist[25][29].collidable = True

tilesetdef.tilelist[25][29].image = tilemap.tilemap[3][3]"""

tilesetdef.aggregate_collidables()
tilesetdef.aggregate_noncollidable()

atrsnak = {
"dmg":5,
"speed":2,
"fov":4,
"special":[],
"hp":30,
"name":"snake"
}
atrlist = [atrsnak]

atrswrd =  {
"dmg":10,
"speed":2,
"fov":4,
"special":[],
"hp": 1,
"name":"sword"
}

atrroot = {"food": 20, "hp":1, "heal":1, "name":"root"}
atrstone = {"dmg": 5, "hp":1, "name":"stone"}
atrpick = {"dmg": 10, "hp":1, "name":"pickaxe"}
atrpot = {"hp":1, "heal":50, "name":"health potion"}
itematrlist = [atrswrd, atrroot, atrstone, atrpick, atrpot]



#snake = tofy.entitytools.entity.Enemy(tilemap.tilemap[1][1], 3, 0, 0.1, batch, foreground, tilesetdef, atrlist)
#snake.listen_to_subject(playerobject)
#print(snake.risk)


worldobject = tofy.world.World([tilesetdef], playerobject, tilemap, batch, background,atrlist, foreground, itematrlist)
worldobject.testworldcreate()
#worldobject.tilesetlist[0] = tilesetdef
centeredcam.position = playerobject.x, playerobject.y
worldobject.checkFOV()

playerobject.push_handlers(worldobject)

gamegui = GameGUI(x, batch, guigroup, centeredcam.position[0] + 240, centeredcam.position[1] - 390, x.width - (0.75 * x.width) + 20, 775)
#gamegui.AddPushButton((200, 200), [tilemap.tilemap[5][6], btnimg], "test_button")
gamegui.AddFeed(200, 200, (0, 500, 0.1), "essa")
gamegui.AddTextLabel((0, 100, 0.1), "invroot", "amount of roots: " + str(playerobject.rootcount) + " PRESS NUM1")
#gamegui.AddTextLabel((0, 150, 0.1), "invstone", "amount of stones: " + str(playerobject.rootcount))
gamegui.AddTextLabel((0, 130, 0.1), "invpot", "amount of health potions: " + str(playerobject.potcount)+ " PRESS NUM3")
gamegui.AddTextLabel((30, 300, 0.1), "hpcount", "Health: " + str(playerobject.atr["hp"]) + "/" + str(playerobject.atr["maxhp"]))
gamegui.AddTextLabel((30, 280, 0.1), "dmgcount", "dmg: " + str(playerobject.atr["dmg"]))
gamegui.AddTextLabel((30, 260, 0.1), "hungercount", "hunger: " + str(playerobject.atr["hunger"]) + "/" + str(playerobject.atr["maxhunger"]))
gamegui.AddTextLabel((30, 240, 0.1), "hungrylabel", " ")
#centeredcam.position = playerobject.x, playerobject.y


#worldobject.tilesetlist[1].tilelist[0][0].collidable = True

#print(worldobject.entitylist)
"""print(len(worldobject.tilesetlist))
print(worldobject.tilesetlist[9].x,worldobject.tilesetlist[9].y)
print(worldobject.tilesetlist[0].y3)"""


#x.run()
#pyglet.clock.schedule(on_update)
pyglet.app.run()
