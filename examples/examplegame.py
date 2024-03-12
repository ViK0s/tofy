"""Simple roguelike game created as a game example for tofy"""




import pyglet
import tofy



class GameWindow(pyglet.window.Window):
    """Basic window class, so that we can manipulate and create events"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.active = 1
    def on_draw(self):
        self.render()
    def render(self):
        self.clear()

        self.pre_render()
        centeredcam.begin()
        batch.draw()
        centeredcam.end()

    def run(self):
        while self.active == 1:
            self.render()
            event = self.dispatch_events()
 
    def pre_render(self):
        pass  
    def on_close(self):
        pyglet.app.exit()
        self.active = 0
        self.close()
    




#Extension of the player class so we can add steering
class GamePlayer(tofy.entitytools.player.Player):
    def __init__(self, window, img, relativex, relativey, z, batch, group, tileset, atr):
        super().__init__(window, img, relativex, relativey, z, batch, group, tileset, atr)

    def attack(self, dmg, name):
        """fired when player is attacked"""
        self.atr["hp"] -= dmg
        gamegui.text.text += "\nYou have been attacked by " + name + " for " + str(dmg) + " dmg"
    
    def checkhp(self):
        """check players hp, so we can either end the game, or fix it when it goes above maxhp """
        if self.atr["hp"] <= 0:
            self.batch = None
            #make a label when you lose, to inform the user
            loselabel = pyglet.text.Label("You lose",
                          font_name='Times New Roman',
                          font_size=32,
                          x=self.x, y=self.y,
                          anchor_x='center', anchor_y='center', batch=guibatch, group=guigroup)
            #close after waiting for a bit
            def callback(lol):
                pyglet.app.exit()
                x.active = 0
                x.close()
            pyglet.clock.schedule_interval(callback, 3)
        #check if the player has more hp than max, if he does, change it to max
        elif self.atr["hp"] > self.atr["maxhp"]:
            self.atr["hp"] =  self.atr["maxhp"]
            gamegui.Update()
    
    def checkhunger(self):
        """check players hunger, so we can write if the player is hungry into the gui, also check if the hunger is not going above maxhunger"""
        
        #reset the "hungry" label so that it's not there if the player is not hungry
        gamegui.elementdict["hungrylabel"].text = " "
        if self.atr["hunger"] <= 0:
            self.atr["hp"] -= 1
            gamegui.elementdict["hungrylabel"].text = "Hungry!"
            gamegui.elementdict["hungrylabel"].color = (205,127,50, 255)
        elif self.atr["hunger"] > self.atr["maxhunger"]:
            self.atr["hunger"] = self.atr["maxhunger"]
    
    def on_key_press(self, symbol, modifiers):
        "handle actions for player input"
        
        #when moving, make sure to adjust the hunger, and check if enemies are colliding with the player
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
            
            #change player position
            self.relativex += 1
            
            #this is a stupid bypass, because I couldn't implement a camera on time, this works, and because of that is used in every
            #control handling from here on out, this way the gui elements can be moved
            dif = abs(playerobject.x - temp)
            
            #update the fov, and player vectors
            self.update_vectors()
            worldobject.checkFOV()
            
            #move the camera
            centeredcam.position = playerobject.x, playerobject.y
            
            #move the gui
            gamegui.x += dif
            
        if symbol == self.key.LEFT and not self.detect_collision(-1, 0, worldobject):
            temp = playerobject.x
            #change player position
            self.relativex -= 1
            #bypass mentioned at line 105
            dif = -abs(playerobject.x - temp)
            
            #update the fov, and player vectors
            self.update_vectors()
            worldobject.checkFOV()
            
            #move the camera
            centeredcam.position = playerobject.x, playerobject.y
            
            #move the gui
            gamegui.x += dif

        if symbol == self.key.UP and not self.detect_collision(0, 1, worldobject):
            temp = playerobject.y
            
            #change player position
            self.relativey += 1
            
            #bypass mentioned at line 105
            dif = abs(playerobject.y - temp)
            
            #update the fov, and player vectors
            self.update_vectors()
            worldobject.checkFOV()
            
            #move the camera
            centeredcam.position = playerobject.x, playerobject.y

            #move the gui
            gamegui.y += dif

        if symbol == self.key.DOWN and not self.detect_collision(0, -1, worldobject):
            temp = playerobject.y
            
            #change player position
            self.relativey -= 1
            
            #bypass mentioned at line 105
            dif = -abs(playerobject.y - temp)

            #update the fov, and player vectors
            self.update_vectors()
            worldobject.checkFOV()
            
            #move the camera
            centeredcam.position = playerobject.x, playerobject.y

            #move the gui
            gamegui.y += dif
        #debug tools
        """if symbol == self.key.SPACE:
            print("relative positions: ",self.relativex, self.relativey, self.tilesetloc)
            print("non relative ones: ", self.x, self.y)
            print(worldobject.entitylist)"""
        #handle input for item usage for root
        if symbol == self.key.NUM_1 and playerobject.rootcount > 0:
            playerobject.remove_item("root")
            playerobject.atr["hp"] += 2
            playerobject.atr["hunger"] += 15
            playerobject.count_items()
            gamegui.Update
        #stones are no longer used
        """if symbol == self.key.NUM_2 and playerobject.stonecount > 0:
            playerobject.remove_item("stone")
            playerobject.count_items()
            gamegui.Update"""
        #handle input for item usage for health_potion
        if symbol == self.key.NUM_3 and playerobject.potcount > 0:
            playerobject.remove_item("health potion")
            playerobject.atr["hp"] += 50
            playerobject.count_items()
            gamegui.Update
        #handle item usage for sword item specifically, so that it can be equiped and deequipped
        if symbol == self.key.NUM_4 and gamegui.indx[0]:
            if playerobject.equipped:
                playerobject.equipped = None
                gamegui.elementdict["itemclick"].setstyle(0, len(gamegui.elementdict["itemclick"]), dict(color=(255, 0, 0, 255)))
            else:
                playerobject.equiped = playerobject.inventory[gamegui.indx[0]]
                gamegui.elementdict["itemclick"].setstyle(0, len(gamegui.elementdict["itemclick"]), dict(color=(0, 255, 0, 255)))

#define game window
x = GameWindow(width = 1024, height = 768, caption="Caverns")



#import tileimg
tileimages = pyglet.resource.image("data/curses_800x600.png")


#create and initialize tilemap object
tilemap = tofy.tiletools.tilemap.Tilemap()
tilemap.create_from_img(tileimages, 16, 16)



#define batches and groups
foreground = pyglet.graphics.Group(order=1)
background = pyglet.graphics.Group(order=0)
guigroup = pyglet.graphics.Group(order=2)
higherguigroup = pyglet.graphics.Group(order=3)
batch = pyglet.graphics.Batch()
guibatch = pyglet.graphics.Batch()


###############################
# Create ingame GUI
###############################
class GameGUI(pyglet.gui.Frame):
    """Object containing all ui elements, and handling events for them"""
    def __init__(self, window, batch, group, x, y, width, height, cell_size=64, order=0 ):
        super().__init__(window, cell_size, order)
        self.batch = batch
        self.group = group
        self.width = width
        self.height = height
        self._x = x
        self._y = y
        
        self.background = pyglet.shapes.BorderedRectangle(x, y, self.width, self.height,border_color = (255, 0, 0, 255),color = (0, 0, 0, 255), batch = self.batch, group = self.group)
        
        #dictionray of all elements inside the class
        self.elementdict = {}

        #make playerobject start listening to the gui
        playerobject.push_handlers(self)

        #list of the indexes of swords so that we know which one we are going to use
        self.indx = []
    def AddPushButton(self, pos:tuple, imglist, name:str):
        """Add a button into the gui"""
        #Make the button
        temp = pyglet.gui.PushButton(self.x + pos[0], self.y + pos[1], imglist[0], imglist[1], batch = self.batch, group = self.group)
        
        #Set event handling
        temp.set_handler("on_press", self.push_button_handler)
        temp.set_handler("on_release", self.relese_button_handler)
        self.add_widget(temp)
        
        #Add to the dictionary of objects
        self.elementdict[name] = temp
    def AddFeed(self, width, height, pos, name):
        """Add a scrolling text feed which you can send text to"""
        #Create a document and set style
        self.text = pyglet.text.document.FormattedDocument(" ")
        self.text.set_style(0, len(self.text.text), dict(color=(255, 0, 0, 255)))
        
        #Create the text layout and set position relative to the background
        temp = pyglet.text.layout.ScrollableTextLayout(self.text, width, height, True, batch= self.batch, group = self.group)
        temp.position = self._x + pos[0], self._y + pos[1], pos[2]

        #Add to the dictionary of objects
        self.elementdict[name] = temp
    """def AddToggleButton(self, pos:tuple, imglist, name:str):
        temp = pyglet.gui.ToggleButton(self.x + pos[0], self.y + pos[1], imglist[0], imglist[1], batch = self.batch, group = self.group)
        temp.set_handler("on_toggle", self.push_button_handler)
        self.add_widget(temp)"""
    
    @property
    def x(self):
        return self._x
    
    #set the x for every element, so that they can follow the camera
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
    
    #set the y for every element, so that they can follow the camera
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
        """Handle the mine event"""
        #check if the text is not too long, if it is, clean it
        if len(self.text.text) > 152:
            self.text.text = " "
        self.text.text += "\nYou chip some stone"
    def on_attack(self, dmg, pos, name, type):
        """Handle the attack event"""
        if len(self.text.text) > 152:
            self.text.text = ""
        #handle the information for items
        if type == tofy.entitytools.entity.Item:
            self.text.text += "\nYou pickup " + name
            self.Update()
            if name == "sword":
                self.AddTextLabel((30, 200, 0.1),"itemclick", "Rusty sword")
                buh = playerobject.inventory[-1]
                self.indx.append(playerobject.inventory.index(buh))
        #handle info for enemies
        elif type == tofy.entitytools.entity.Enemy:
            self.text.text += "\nYou attack " + name +" for " + str(dmg) + " damage"
    def AddTextLabel(self, pos, name, string):
        """Add a simple text"""
        temp = pyglet.text.Label(string,
                          font_name='Times New Roman',
                          font_size=12,
                          x=self._x + pos[0], y=self._y + pos[1],
                          anchor_x='left', anchor_y='bottom', batch=self.batch, group=self.group)
        self.elementdict[name] = temp
    def Update(self):
        """Update the gui information"""
        playerobject.count_items()
        self.elementdict["invroot"].text = "amount of roots: " + str(playerobject.rootcount) + " PRESS NUM1"
        #self.elementdict["invstone"].text = "amount of stones: " + str(playerobject.stonecount)
        self.elementdict["invpot"].text = "amount of health potions: " + str(playerobject.potcount) + " PRESS NUM3"
        self.elementdict["hpcount"].text = "Health: " + str(playerobject.atr["hp"]) + "/" + str(playerobject.atr["maxhp"])
        self.elementdict["dmgcount"].text = "dmg: " + str(playerobject.atr["dmg"])
        self.elementdict["hungercount"].text = "hunger: " + str(playerobject.atr["hunger"]) + "/" + str(playerobject.atr["maxhunger"])

    def out_of_bounds(self):
        """Add text informing there's no more terrain"""
        if len(self.text.text) > 152:
            self.text.text = ""
        self.text.text += "\nThere's a chasm before you..."



#Call the camera
centeredcam = tofy.camera.CenteredCamera(x, 20)

#Call the first tileset and fill it
tilesetdef = tofy.tiletools.tileset.Tileset(20, 20, 30, 30, tilemap, None, background, [4, 10])
esa = tilesetdef.createsquarefilled(1, 4)

tilesetdef.aggregate_collidables()
tilesetdef.aggregate_noncollidable()


#Dictionary of attributes for the player character
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

#Call the player class and create events, also count if there are any items in the inventory 
playerobject = GamePlayer(x, tilemap.tilemap[15][1], 10, 10, 0.1, batch, foreground, tilesetdef, plratr)
playerobject.create_new_topic("on_attack")
playerobject.create_new_topic("on_tileset_change")
playerobject.create_new_topic("mine")
playerobject.create_new_topic("out_of_bounds")
playerobject.count_items


#tilesetdef.aggregate_collidables()
#tilesetdef.aggregate_noncollidable()

"""Attributes of enemies and items, agregatted into lists so that we can use them later on"""

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



#Create the world
worldobject = tofy.world.World([tilesetdef], playerobject, tilemap, batch, background,atrlist, foreground, itematrlist)
worldobject.testworldcreate()
centeredcam.position = playerobject.x, playerobject.y
worldobject.checkFOV()

#push player events into the world object
playerobject.push_handlers(worldobject)


#create the gui
gamegui = GameGUI(x, batch, guigroup, centeredcam.position[0] + 240, centeredcam.position[1] - 390, x.width - (0.75 * x.width) + 20, 775)
gamegui.AddFeed(200, 200, (0, 500, 0.1), "essa")
gamegui.AddTextLabel((0, 100, 0.1), "invroot", "amount of roots: " + str(playerobject.rootcount) + " PRESS NUM1")
#gamegui.AddTextLabel((0, 150, 0.1), "invstone", "amount of stones: " + str(playerobject.rootcount))
gamegui.AddTextLabel((0, 130, 0.1), "invpot", "amount of health potions: " + str(playerobject.potcount)+ " PRESS NUM3")
gamegui.AddTextLabel((30, 300, 0.1), "hpcount", "Health: " + str(playerobject.atr["hp"]) + "/" + str(playerobject.atr["maxhp"]))
gamegui.AddTextLabel((30, 280, 0.1), "dmgcount", "dmg: " + str(playerobject.atr["dmg"]))
gamegui.AddTextLabel((30, 260, 0.1), "hungercount", "hunger: " + str(playerobject.atr["hunger"]) + "/" + str(playerobject.atr["maxhunger"]))
gamegui.AddTextLabel((30, 240, 0.1), "hungrylabel", " ")



pyglet.app.run()
