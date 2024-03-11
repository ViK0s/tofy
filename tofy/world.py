from tofy import tiletools
from tiletools import tileset
from entitytools import entity
import random

class World():
    def __init__(self, tilesetlist, player, tilemap, batch, group, atrlist, entitygroup, itematrlist):
        self.tilesetlist = tilesetlist
        self.player = player
        
        #list of a list of enemies, coordinates are tileset based, meaning index = 0 is the first tileset
        self.entitylist = []
        

        self.visibletiles = []
        self.tilemap = tilemap
        self.batch = batch
        self.group = group


        self.x = self.tilesetlist[0].x
        self.y = self.tilesetlist[0].y
        # a list of attributes so that we know what enemies to create
        self.atrlist = atrlist
        self.entitygroup = entitygroup

        self.itematrlist = itematrlist
    """
    a really inefficient implementation of raycasting, this will need a major rework, but it doesn't lag so it's
    fine for now?
    """
    """
    This was supposed to be able to check chunks that are next to the current player chunk
    but this idea proved really hard to do, not that efficient and with ALOT of edge cases
    (for example, know which corner ur at, checking if walls are infront when checking the next chunk etc.)
    """
    
    """def checkFOV(self):
        currenttileset = self.player.tilesetloc
        
        #loop through tiles that were visible and make them invisible so the player knows which ones are unactive
        for i in self.tilesetlist[currenttileset].tilelist:
                for n in i:
                    n.visiblebyplayer = False
        
        
        # but check first which tilesets should the computation be for
        
            
        
        #do the same for entities
        for i in self.entitylist:
            i.visible = False
        
        # lists of the points that are visible
        top = []
        down = []
        left = []
        right = []

        allpoints = []
        nextpointsright = []
        nextpointsbelow = []
        nextpointsbelowright = []


        nextpointstop = []
        nextpointsleft = []
        nextpointsrighttop = []
        # cast rays to points of interests, here it casts them all from the player to the max range
        for i in range(self.player.relativex - self.player.FOVrange, self.player.relativex + self.player.FOVrange):
            top = self.bresenhamLOS(self.player.relativex, self.player.relativey, i, self.player.relativey + self.player.FOVrange)
            down = self.bresenhamLOS(self.player.relativex, self.player.relativey, i, self.player.relativey - self.player.FOVrange)
            allpoints.append(top)
            allpoints.append(down)

        for i in range(self.player.relativey - self.player.FOVrange, self.player.relativey + self.player.FOVrange):
            left = self.bresenhamLOS(self.player.relativex, self.player.relativey, self.player.relativex - self.player.FOVrange, i)
            right = self.bresenhamLOS(self.player.relativex, self.player.relativey, self.player.relativex + self.player.FOVrange, i)
            allpoints.append(left)
            allpoints.append(right)
        
        #situation where the player is close to the border of tileset on the bottom right
        if self.player.magnitude3 > self.player.magnitude2 and self.player.relativex > (self.player.tileset.width // 2):
            #make the tiles be not visible
            for i in self.tilesetlist[currenttileset + 1].tilelist:
                for n in i:
                    n.visiblebyplayer = False
            
            #check the visibility in the tileset to the right
            for i in range(self.player.relativey - self.player.FOVrange, self.player.relativey + self.player.FOVrange):
                right = self.bresenhamLOS(self.player.relativex - self.player.tileset.width, self.player.relativey, (self.player.relativex - self.player.tileset.width) + self.player.FOVrange, i)
                nextpointsright.append(right)
            
            for i in range((self.player.relativex - self.player.tileset.width) - self.player.FOVrange, (self.player.relativex - self.player.tileset.width) + self.player.FOVrange):
                down = self.bresenhamLOS(self.player.relativex - self.player.tileset.width, self.player.relativey, i, self.player.relativey - self.player.FOVrange)
                top = self.bresenhamLOS(self.player.relativex - self.player.tileset.width, self.player.relativey, i, self.player.relativey + self.player.FOVrange)
                nextpointsright.append(down)
                nextpointsright.append(top)
            

            for i in self.tilesetlist[currenttileset + 1].tilelist:
                for n in i:
                    for k in nextpointsright:
                        for bruh in k:
                            if bruh == n.relativepos:
                                n.batch = self.tilesetlist[currenttileset + 1].batch
                                n.visiblebyplayer = True


            
            #check if there are tiles below, if not, skip
            #this seems really inefficient
                #it's -9 because the list is 1D and every 9 tiles the tile goes up
            if currenttileset - 9 >= 0:
                #check the visibility for the tileset below
                for i in range((self.player.relativey + self.player.tileset.height) - self.player.FOVrange, (self.player.relativey + self.player.tileset.height) + self.player.FOVrange):
                    left = self.bresenhamLOS(self.player.relativex, self.player.relativey + self.player.tileset.height, self.player.relativex - self.player.FOVrange, i)
                    right = self.bresenhamLOS(self.player.relativex, self.player.relativey + self.player.tileset.height, self.player.relativex + self.player.FOVrange, i)
                    nextpointsbelow.append(left)
                    nextpointsbelow.append(right)
                
                for i in range(self.player.relativex - self.player.FOVrange, self.player.relativex + self.player.FOVrange):
                    down = self.bresenhamLOS(self.player.relativex - self.player.tileset.width, self.player.relativey, i, self.player.relativey - self.player.FOVrange)
                    nextpointsbelow.append(down)
                
                for i in self.tilesetlist[currenttileset - 9].tilelist:
                    for n in i:
                        for k in nextpointsbelow:
                            for bruh in k:
                                if bruh == n.relativepos:
                                    n.batch = self.tilesetlist[currenttileset - 10].batch
                                    n.visiblebyplayer = True

                #check the visibility for the tileset on the below right corner
                for i in range((self.player.relativey + self.player.tileset.height) - self.player.FOVrange, (self.player.relativey + self.player.tileset.height) + self.player.FOVrange):
                    right = self.bresenhamLOS(self.player.relativex - self.player.tileset.width, self.player.relativey + self.player.tileset.height, (self.player.relativex - self.player.tileset.width) + self.player.FOVrange, i)
                    nextpointsbelowright.append(right)
                
                
                for i in range((self.player.relativex - self.player.tileset.width) - self.player.FOVrange, (self.player.relativex - self.player.tileset.width) + self.player.FOVrange):
                    down = self.bresenhamLOS(self.player.relativex - self.player.tileset.width, self.player.relativey + self.player.tileset.height, i, (self.player.relativey + self.player.tileset.height) - self.player.FOVrange)
                    nextpointsbelowright.append(down)
            
                for i in self.tilesetlist[currenttileset - 9].tilelist:
                    for n in i:
                        for k in nextpointsbelowright:
                            for bruh in k:
                                if bruh == n.relativepos:
                                    n.batch = self.tilesetlist[currenttileset - 10].batch
                                    n.visiblebyplayer = True

        #situation where we are on the bottom left
        elif self.player.magnitude3 > self.player.magnitude2 and self.player.relativex < (self.player.tileset.width // 2):
            
            #check the tileset to the left
            if currenttileset - 1 >= 0:
                #make the tiles invisible
                for i in self.tilesetlist[currenttileset - 1].tilelist:
                    for n in i:
                        n.visiblebyplayer = False
                
                for i in range(self.player.relativey - self.player.FOVrange, self.player.relativey + self.player.FOVrange):
                    left = self.bresenhamLOS(self.player.relativex + self.player.tileset.width, self.player.relativey, (self.player.relativex + self.player.tileset.width) - self.player.FOVrange, i)
                    nextpointsleft.append(left)
            
                for i in range((self.player.relativex + self.player.tileset.width) - self.player.FOVrange, (self.player.relativex + self.player.tileset.width) + self.player.FOVrange):
                    down = self.bresenhamLOS(self.player.relativex + self.player.tileset.width, self.player.relativey, i, self.player.relativey - self.player.FOVrange)
                    top = self.bresenhamLOS(self.player.relativex + self.player.tileset.width, self.player.relativey, i, self.player.relativey + self.player.FOVrange)
                    nextpointsleft.append(down)
                    nextpointsleft.append(top)
                

                for i in self.tilesetlist[currenttileset - 1].tilelist:
                    for n in i:
                        for k in nextpointsleft:
                            for bruh in k:
                                if bruh == n.relativepos:
                                    n.batch = self.tilesetlist[currenttileset - 1].batch
                                    n.visiblebyplayer = True
            
            #check tileset to the bottom
            #skip if no tileset below
            if currenttileset - 9 >= 0:
                #check the visibility for the tileset below
                for i in range((self.player.relativey + self.player.tileset.height) - self.player.FOVrange, (self.player.relativey + self.player.tileset.height) + self.player.FOVrange):
                    left = self.bresenhamLOS(self.player.relativex, self.player.relativey + self.player.tileset.height, self.player.relativex - self.player.FOVrange, i)
                    right = self.bresenhamLOS(self.player.relativex, self.player.relativey + self.player.tileset.height, self.player.relativex + self.player.FOVrange, i)
                    nextpointsbelow.append(left)
                    nextpointsbelow.append(right)
                
                for i in range(self.player.relativex - self.player.FOVrange, self.player.relativex + self.player.FOVrange):
                    down = self.bresenhamLOS(self.player.relativex, self.player.relativey + self.player.tileset.height, i, (self.player.relativey + self.player.tileset.height) - self.player.FOVrange)
                    nextpointsbelow.append(down)
                
                for i in self.tilesetlist[currenttileset - 9].tilelist:
                    for n in i:
                        for k in nextpointsbelow:
                            for bruh in k:
                                if bruh == n.relativepos:
                                    n.batch = self.tilesetlist[currenttileset - 9].batch
                                    n.visiblebyplayer = True

                #check the visibility for the tileset on the below left corner
                for i in range((self.player.relativey + self.player.tileset.height) - self.player.FOVrange, (self.player.relativey + self.player.tileset.height) + self.player.FOVrange):
                    left = self.bresenhamLOS(self.player.relativex + self.player.tileset.width, self.player.relativey + self.player.tileset.height, (self.player.relativex + self.player.tileset.width) + self.player.FOVrange, i)
                    nextpointsbelowright.append(right)
                

                for i in range((self.player.relativex + self.player.tileset.width) - self.player.FOVrange, (self.player.relativex + self.player.tileset.width) + self.player.FOVrange):
                    down = self.bresenhamLOS(self.player.relativex + self.player.tileset.width, self.player.relativey + self.player.tileset.height, i, (self.player.relativey + self.player.tileset.height) - self.player.FOVrange)
                    nextpointsbelowright.append(down)
            
                for i in self.tilesetlist[currenttileset - 10].tilelist:
                    for n in i:
                        for k in nextpointsbelowright:
                            for bruh in k:
                                if bruh == n.relativepos:
                                    n.batch = self.tilesetlist[currenttileset - 10].batch
                                    n.visiblebyplayer = True
        
        #situation where we are on the top right and want to see the tile to the top, right, and top right
        elif self.player.magnitude3 < self.player.magnitude2 and self.player.relativex > (self.player.tileset.width // 2):
            #make the tiles be not visible
            for i in self.tilesetlist[currenttileset + 1].tilelist:
                for n in i:
                    n.visiblebyplayer = False
            
            #check the visibility in the tileset to the right
            for i in range(self.player.relativey - self.player.FOVrange, self.player.relativey + self.player.FOVrange):
                right = self.bresenhamLOS(self.player.relativex - self.player.tileset.width, self.player.relativey, (self.player.relativex - self.player.tileset.width) + self.player.FOVrange, i)
                nextpointsright.append(right)
            
            for i in range((self.player.relativex - self.player.tileset.width) - self.player.FOVrange, (self.player.relativex - self.player.tileset.width) + self.player.FOVrange):
                down = self.bresenhamLOS(self.player.relativex - self.player.tileset.width, self.player.relativey, i, self.player.relativey - self.player.FOVrange)
                top = self.bresenhamLOS(self.player.relativex - self.player.tileset.width, self.player.relativey, i, self.player.relativey + self.player.FOVrange)
                nextpointsright.append(down)
                nextpointsright.append(top)
            

            for i in self.tilesetlist[currenttileset + 1].tilelist:
                for n in i:
                    for k in nextpointsright:
                        for bruh in k:
                            if bruh == n.relativepos:
                                n.batch = self.tilesetlist[currenttileset + 1].batch
                                n.visiblebyplayer = True
            #check the top tileset
            #first check if there even are tiles to check, if not skip
            if currenttileset + 9 <= self.maxtileset:
                for i in self.tilesetlist[currenttileset + 9].tilelist:
                    for n in i:
                        n.visiblebyplayer = False
                for i in range((self.player.relativey - self.player.tileset.height) - self.player.FOVrange, (self.player.relativey - self.player.tileset.height) + self.player.FOVrange):
                    right = self.bresenhamLOS(self.player.relativex, self.player.relativey - self.player.tileset.height, self.player.relativex + self.player.FOVrange, i)
                    left = self.bresenhamLOS(self.player.relativex, self.player.relativey - self.player.tileset.height, self.player.relativex - self.player.FOVrange, i)
                    nextpointstop.append(left)
                    nextpointstop.append(right)

                for i in range(self.player.relativex - self.player.FOVrange, self.player.relativex + self.player.FOVrange):
                    top = self.bresenhamLOS(self.player.relativex, self.player.relativey - self.player.tileset.height, i, (self.player.relativey - self.player.tileset.height) + self.player.FOVrange)
                    nextpointstop.append(top)

                for i in self.tilesetlist[currenttileset + 9].tilelist:
                    for n in i:
                        for k in nextpointstop:
                            for bruh in k:
                                if bruh == n.relativepos:
                                    n.batch = self.tilesetlist[currenttileset + 9].batch
                                    n.visiblebyplayer = True
                #check the top right tileset
                
                for i in self.tilesetlist[currenttileset + 10].tilelist:
                    for n in i:
                        n.visiblebyplayer = False

                for i in range((self.player.relativey - self.player.tileset.height) - self.player.FOVrange, (self.player.relativey - self.player.tileset.height) + self.player.FOVrange):
                    right = self.bresenhamLOS((self.player.relativex - self.player.tileset.width), self.player.relativey - self.player.tileset.height, (self.player.relativex - self.player.tileset.width) + self.player.FOVrange, i)
                    nextpointsrighttop.append(right)

                for i in range((self.player.relativex - self.player.tileset.width) - self.player.FOVrange, (self.player.relativex - self.player.tileset.width) + self.player.FOVrange):
                    top = self.bresenhamLOS((self.player.relativex - self.player.tileset.width), self.player.relativey - self.player.tileset.height, i, (self.player.relativey - self.player.tileset.height) + self.player.FOVrange)
                    nextpointsrighttop.append(top)       

                for i in self.tilesetlist[currenttileset + 10].tilelist:
                    for n in i:
                        for k in nextpointsrighttop:
                            for bruh in k:
                                if bruh == n.relativepos:
                                    n.batch = self.tilesetlist[currenttileset + 10].batch
                                    n.visiblebyplayer = True
        
        #situation where we are on the top left
        elif self.player.magnitude3 < self.player.magnitude2 and self.player.relativex < (self.player.tileset.width // 2):
            #make the tiles invisible
            for i in self.tilesetlist[currenttileset - 1].tilelist:
                for n in i:
                    n.visiblebyplayer = False
            #check the tileset to the left
            if currenttileset - 1 >= 0:
                
                for i in range(self.player.relativey - self.player.FOVrange, self.player.relativey + self.player.FOVrange):
                    left = self.bresenhamLOS(self.player.relativex + self.player.tileset.width, self.player.relativey, (self.player.relativex + self.player.tileset.width) - self.player.FOVrange, i)
                    nextpointsleft.append(left)
            
                for i in range((self.player.relativex + self.player.tileset.width) - self.player.FOVrange, (self.player.relativex + self.player.tileset.width) + self.player.FOVrange):
                    down = self.bresenhamLOS(self.player.relativex + self.player.tileset.width, self.player.relativey, i, self.player.relativey - self.player.FOVrange)
                    top = self.bresenhamLOS(self.player.relativex + self.player.tileset.width, self.player.relativey, i, self.player.relativey + self.player.FOVrange)
                    nextpointsleft.append(down)
                    nextpointsleft.append(top)
                

                for i in self.tilesetlist[currenttileset - 1].tilelist:
                    for n in i:
                        for k in nextpointsleft:
                            for bruh in k:
                                if bruh == n.relativepos:
                                    n.batch = self.tilesetlist[currenttileset - 1].batch
                                    n.visiblebyplayer = True
            
        
        #part outside the big if statement
        for i in self.tilesetlist[currenttileset].tilelist:
            for n in i:
                for k in allpoints:
                    for bruh in k:
                        if bruh == n.relativepos:
                            n.batch = self.tilesetlist[currenttileset].batch
                            n.visiblebyplayer = True


        for i in self.entitylist:
            for k in allpoints:
                    for bruh in k:
                        if bruh == (i.relativex, i.relativey):
                            i.batch = self.tilesetlist[currenttileset].batch
                            i.visible = True"""
                
    # implementation of bresenham line algorithm
    # based on the official python library with the same name
    # with slight modification to account for visibility and different type return
    # this will need a rework to account for visibility range
    def checkFOV(self):
        currenttileset = self.player.tilesetloc
        
        #loop through tiles that were visible and make them invisible so the player knows which ones are unactive
        for i in self.tilesetlist[currenttileset].tilelist:
                for n in i:
                    n.visiblebyplayer = False
        #do the same for entities
        for i in self.entitylist:
            i.visible = False
        


        #clean tiles when switching to new tileset
        


        # lists of the points that are visible
        top = []
        down = []
        left = []
        right = []

        allpoints = []


        # cast rays to points of interests, here it casts them all from the player to the max range
        for i in range(self.player.relativex - self.player.FOVrange, self.player.relativex + self.player.FOVrange):
            top = self.bresenhamLOS(self.player.relativex, self.player.relativey, i, self.player.relativey + self.player.FOVrange)
            down = self.bresenhamLOS(self.player.relativex, self.player.relativey, i, self.player.relativey - self.player.FOVrange)
            allpoints.append(top)
            allpoints.append(down)

        for i in range(self.player.relativey - self.player.FOVrange, self.player.relativey + self.player.FOVrange):
            left = self.bresenhamLOS(self.player.relativex, self.player.relativey, self.player.relativex - self.player.FOVrange, i)
            right = self.bresenhamLOS(self.player.relativex, self.player.relativey, self.player.relativex + self.player.FOVrange, i)
            allpoints.append(left)
            allpoints.append(right)

        for i in self.tilesetlist[currenttileset].tilelist:
            for n in i:
                for k in allpoints:
                    for bruh in k:
                        if bruh == n.relativepos:
                            n.batch = self.tilesetlist[currenttileset].batch
                            n.visiblebyplayer = True

        
        for i in self.entitylist:
            for k in allpoints:
                    for bruh in k:
                        if bruh == (i.relativex, i.relativey) and i.tilesetloc == self.player.tilesetloc:
                            i.batch = self.tilesetlist[currenttileset].batch
                            i.visible = True


    def bresenhamLOS(self, x0, y0, x1, y1):
    
        dx = x1 - x0
        dy = y1 - y0

        xsign = 1 if dx > 0 else -1
        ysign = 1 if dy > 0 else -1

        dx = abs(dx)
        dy = abs(dy)

        if dx > dy:
            xx, xy, yx, yy = xsign, 0, 0, ysign
        else:
            dx, dy = dy, dx
            xx, xy, yx, yy = 0, ysign, xsign, 0

        D = 2*dy - dx
        y = 0
        points = []
        for x in range(dx + 1):
            current = (x0 + x*xx + y*yx, y0 + x*xy + y*yy)
            if current[0] >= 0 and current[1] >= 0:
                points.append(current)
            """
            loop through the y and then x axis of tilelist and check if the tile is a collidable
            if it is, don't print any more points
            """
            """for i in self.tilesetlist[0].tilelist:
                for n in i:
                    if n.relativepos == current and n.collidable == True:
                        return points"""
            for i in self.tilesetlist[self.player.tilesetloc].collidabletiles:
                if i.relativepos == current:
                    return points
            
            
            if D >= 0:
                y += 1
                D -= 2*dx
            D += 2*dy
        return points
    
    def testworldcreate(self):
        temporary = self.tilesetlist[0]
        self.tilesetlist = []
        x = self.x
        y = self.y

        

        #the range is the max lenght of the 1D list
        for height in range(0, 9):
                


                for width in range(0, 9):   #self.tilemap.tile_width+self.tilespace[0]
                    index = width + 10 * height
                    caveornot = random.randint(0, 1)
                    if caveornot == 0:
                        temp = tileset.Tileset(x + (width*temporary.x2), y + (height * temporary.y3), 30, 30, self.tilemap, self.batch, self.group, [4, 10])
                        temp.createsquarefilled(2, 4)
                        temp.aggregate_collidables()
                        temp.aggregate_noncollidable()
                        self.tilesetlist.append(temp)
                    else:
                        temp = tileset.Tileset(x + (width*temporary.x2), y + (height * temporary.y3), 30, 30, self.tilemap, self.batch, self.group, [4, 10])
                        temp.gen_cave()
                        temp.aggregate_collidables()
                        temp.aggregate_noncollidable()
                        self.tilesetlist.append(temp)
                        
                        #self.populate(temp, len(self.tilesetlist) - 1)
                    
                    
        self.maxtileset = len(self.tilesetlist) - 1
        self.spawnplayer()
    def cleantileset(self, tilesetindex):
        for i in self.tilesetlist[tilesetindex].tilelist:
            for n in i:
                n.visiblebyplayer = False

    def on_tileset_change(self, tilesetindex):
        #print("changed tileset", tilesetindex)
        self.cleantileset(tilesetindex)

    def populate(self, tilesetindex):
        

        risk = 0
        #check what type of encounter there will be
        # type 1 is enemy infested, type 2 is risky,  type 3 is clear
        encountertype = random.randint(1, 3)
        #maxrisk and maxreward are random integers that say what tf can even be generated
        if encountertype == 1 and self.tilesetlist[tilesetindex].unexplored:
            enemycount = random.randint(1, 4)
            randpos = random.randint(0, len(self.tilesetlist[tilesetindex].noncollidabletiles))    
            randenemy = random.randint(0, len(self.atrlist))
            for i in range(0, enemycount):
                randpos = random.randint(0, len(self.tilesetlist[tilesetindex].noncollidabletiles))
                enemy = entity.Enemy(self.tilemap.tilemap[1][1], self.tilesetlist[tilesetindex].noncollidabletiles[randpos-1].relativepos[0], self.tilesetlist[tilesetindex].noncollidabletiles[randpos-1].relativepos[1], 0.1, self.batch, self.entitygroup, self.tilesetlist[tilesetindex], self.atrlist[randenemy-1])
                enemy.create_new_topic("attack")
                enemy.push_handlers(self.player)
                enemy.tilesetloc = tilesetindex
                enemy.listen_to_subject(self.player)
                self.entitylist.append(enemy)
                self.tilesetlist[tilesetindex].noncollidabletiles.pop(randpos)
        
        elif encountertype == 2 and self.tilesetlist[tilesetindex].unexplored:
            enemycount = random.randint(1, 4)
            randpos = random.randint(0, len(self.tilesetlist[tilesetindex].noncollidabletiles))    
            randenemy = random.randint(0, len(self.atrlist))
            for i in range(0, enemycount):
                randpos = random.randint(0, len(self.tilesetlist[tilesetindex].noncollidabletiles))
                enemy = entity.Enemy(self.tilemap.tilemap[1][1], self.tilesetlist[tilesetindex].noncollidabletiles[randpos-1].relativepos[0], self.tilesetlist[tilesetindex].noncollidabletiles[randpos-1].relativepos[1], 0.1, self.batch, self.entitygroup, self.tilesetlist[tilesetindex], self.atrlist[randenemy-1])
                enemy.create_new_topic("attack")
                enemy.push_handlers(self.player)
                #enemy.settileset(tilesetindex, self.tilesetlist[tilesetindex], self.tilesetlist[tilesetindex].noncollidabletiles[randpos].relativepos[0], self.tilesetlist[tilesetindex].noncollidabletiles[randpos].relativepos[1])
                #temp.append(enemy)
                enemy.tilesetloc = tilesetindex
                enemy.listen_to_subject(self.player)
                
                self.entitylist.append(enemy)
                self.tilesetlist[tilesetindex].noncollidabletiles.pop(randpos)
                #risk += enemy.risk
                
                #maxreward = random.randint(risk, 100 + risk)
            randpos = random.randint(0, len(self.tilesetlist[tilesetindex].noncollidabletiles))
            item = entity.Item(self.tilemap.tilemap[5][0], self.tilesetlist[tilesetindex].noncollidabletiles[randpos-1].relativepos[0], self.tilesetlist[tilesetindex].noncollidabletiles[randpos-1].relativepos[1], 0.1, self.batch, self.entitygroup, self.tilesetlist[tilesetindex], self.itematrlist[randenemy-1])
            
            item.tilesetloc = tilesetindex
            item.listen_to_subject(self.player)

            self.entitylist.append(item)
            
        self.tilesetlist[tilesetindex].unexplored = False     

            
            
    def on_attack(self, dmg, atkpos, name, loltype):
        for i in self.entitylist:
            if i.relativex == atkpos[0] and i.relativey == atkpos[1]:
                i.hp -= dmg
                if i.hp <= 0 and type(i) == entity.Enemy:
                    rand = random.randint(0, 15)
                    if rand == 15:
                        self.entitylist.append(entity.Item(self.tilemap.tilemap[5][0],i.relativex ,i.relativey, 0.1, self.batch, self.entitygroup, i.tileset, self.itematrlist[4]))
                    self.entitylist.remove(i)
                elif i.hp <= 0 and type(i) == entity.Item:
                    i.batch = None
                    self.player.inventory.append(i)
                    self.entitylist.remove(i)


    def mine(self, pos, tilesetloc):
        self.tilesetlist[tilesetloc].tilelist[pos[0]][pos[1]].hp -= 1
        if self.tilesetlist[tilesetloc].tilelist[pos[0]][pos[1]].hp <= 0:
            self.tilesetlist[tilesetloc].tilelist[pos[0]][pos[1]].collidable = False
            self.tilesetlist[tilesetloc].tilelist[pos[0]][pos[1]].image = self.tilemap.tilemap[4][1]
            self.tilesetlist[tilesetloc].aggregate_collidables()
            rand = random.randint(0, 1)
            if rand == 1:
            #    randomitem = random.randint(1, 2)
                self.entitylist.append(entity.Item(self.tilemap.tilemap[5][0],pos[1] ,pos[0], 0.1, self.batch, self.entitygroup, self.tilesetlist[tilesetloc], self.itematrlist[1]))
        
    def enemymovement(self):
        allpoints = []
        for entit in self.entitylist:
            if type(entit) == entity.Enemy and entit.tilesetloc == self.player.tilesetloc:
                for i in range(entit.relativex - entit.attributes["fov"], entit.relativex + entit.attributes["fov"]):
                    top = self.bresenhamLOS(entit.relativex, entit.relativey, i, entit.relativey + entit.attributes["fov"])
                    down = self.bresenhamLOS(entit.relativex, entit.relativey, i, entit.relativey - entit.attributes["fov"])
                    allpoints.append(top)
                    allpoints.append(down)

                for i in range(entit.relativey - entit.attributes["fov"], entit.relativey + entit.attributes["fov"]):
                    left = self.bresenhamLOS(entit.relativex, entit.relativey, entit.relativex - entit.attributes["fov"], i)
                    right = self.bresenhamLOS(entit.relativex, entit.relativey, entit.relativex + entit.attributes["fov"], i)
                    allpoints.append(left)
                    allpoints.append(right)
                moves = self.bresenhamLOS(entit.relativex, entit.relativey, self.player.relativex, self.player.relativey)
                for i in allpoints:
                    for k in i:
                        if k == (self.player.relativex, self.player.relativey):
                            #moves = self.bresenhamLOS(entit.relativex, entit.relativey, self.player.relativex, self.player.relativey)
                            #print(moves[0][0], moves[0][1])
                            if len(moves) == 1:
                                return
                            if moves[1] != (self.player.relativex, self.player.relativey):
                                entit.relativex = moves[1][0]
                                entit.relativey = moves[1][1]
                    
                    #if moves[1] == (self.player.relativex, self.player.relativey):
                        #self.player.atr["hp"] =- entit.attributes["dmg"]
    def spawnplayer(self):
        for tileset in self.tilesetlist:
            index = self.tilesetlist.index(tileset)
            if len(tileset.noncollidabletiles) > 5:
                tileset.unexplored = False
                randpos = random.randint(0, len(self.tilesetlist[index].noncollidabletiles))
                self.player.settileset(index, tileset, self.tilesetlist[index].noncollidabletiles[randpos-1].relativepos[0], self.tilesetlist[index].noncollidabletiles[randpos-1].relativepos[1])