from tofy import tiletools
from tiletools import tileset


class World():
    def __init__(self, tilesetlist, player, entitylist, tilemap, batch, group):
        self.tilesetlist = tilesetlist
        self.player = player
        self.entitylist = entitylist
        self.visibletiles = []
        self.tilemap = tilemap
        self.batch = batch
        self.group = group
    
    """
    a really inefficient implementation of raycasting, this will need a major rework, but it doesn't lag so it's
    fine for now?
    """
    def checkFOV(self):
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

        nextpointsleft = []
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
                #it's -10 because the list is 1D and every 10 tiles the tile goes up
            if currenttileset - 10 >= 0:
                #check the visibility for the tileset below
                for i in range((self.player.relativey + self.player.tileset.height) - self.player.FOVrange, (self.player.relativey + self.player.tileset.height) + self.player.FOVrange):
                    left = self.bresenhamLOS(self.player.relativex, self.player.relativey + self.player.tileset.height, self.player.relativex - self.player.FOVrange, i)
                    right = self.bresenhamLOS(self.player.relativex, self.player.relativey + self.player.tileset.height, self.player.relativex + self.player.FOVrange, i)
                    nextpointsbelow.append(left)
                    nextpointsbelow.append(right)
                
                for i in range(self.player.relativex - self.player.FOVrange, self.player.relativex + self.player.FOVrange):
                    down = self.bresenhamLOS(self.player.relativex - self.player.tileset.width, self.player.relativey, i, self.player.relativey - self.player.FOVrange)
                    nextpointsbelow.append(down)
                
                for i in self.tilesetlist[currenttileset - 10].tilelist:
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
            
            #check tileset to the bottom
            #skip if no tileset below
            if currenttileset - 10 >= 0:
                #check the visibility for the tileset below
                for i in range((self.player.relativey + self.player.tileset.height) - self.player.FOVrange, (self.player.relativey + self.player.tileset.height) + self.player.FOVrange):
                    left = self.bresenhamLOS(self.player.relativex, self.player.relativey + self.player.tileset.height, self.player.relativex - self.player.FOVrange, i)
                    right = self.bresenhamLOS(self.player.relativex, self.player.relativey + self.player.tileset.height, self.player.relativex + self.player.FOVrange, i)
                    nextpointsbelow.append(left)
                    nextpointsbelow.append(right)
                
                for i in range(self.player.relativex - self.player.FOVrange, self.player.relativex + self.player.FOVrange):
                    down = self.bresenhamLOS(self.player.relativex, self.player.relativey + self.player.tileset.height, i, (self.player.relativey + self.player.tileset.height) - self.player.FOVrange)
                    nextpointsbelow.append(down)
                
                for i in self.tilesetlist[currenttileset - 10].tilelist:
                    for n in i:
                        for k in nextpointsbelow:
                            for bruh in k:
                                if bruh == n.relativepos:
                                    n.batch = self.tilesetlist[currenttileset - 10].batch
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
        #situation where we are on the top right
        if self.player.magnitude3 < self.player.magnitude2 and self.player.relativex > (self.player.tileset.width // 2):
            pass
        #situation where we are on the top left
        elif self.player.magnitude3 < self.player.magnitude2 and self.player.relativex < (self.player.tileset.width // 2):
            pass
        
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
                            i.visible = True
                
    # implementation of bresenham line algorithm
    # based on the official python library with the same name
    # with slight modification to account for visibility and different type return
    # this will need a rework to account for visibility range
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
        for height in range(1, 5):
                for width in range(1, 5):   #self.tilemap.tile_width+self.tilespace[0]
                    temp = tileset.Tileset(self.tilesetlist[width - 1].x2, self.tilesetlist[height - 1].y2, 30, 30, self.tilemap, self.batch, self.group, [4, 10])
                    temp.createsquare(2, 2)
                    self.tilesetlist.append(temp)