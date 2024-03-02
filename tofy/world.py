

class World():
    def __init__(self, tilesetlist, player, entitylist):
        self.tilesetlist = tilesetlist
        self.player = player
        self.entitylist = entitylist
        self.visibletiles = []
    """
    a really inefficient implementation of raycasting, this will need a major rework, but it doesn't lag so it's
    fine for now?
    """
    def checkFOV(self):
        #loop through tiles that were visible and make them invisible so the player knows which ones are unactive
        for i in self.tilesetlist[0].tilelist:
            for n in i:
                n.visiblebyplayer = False
        #do the same for entities
        for i in self.entitylist:
            i.visible = False
        
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

        # this is the version that casts the rays over the whole map
        """ for i in range(0, self.tilesetlist[0].width):
            top = self.bresenhamLOS(self.player.relativex, self.player.relativey, i, self.tilesetlist[0].height, 5)
            down = self.bresenhamLOS(self.player.relativex, self.player.relativey, i, 0, 5)
            allpoints.append(top)
            allpoints.append(down)
 
        
        for i in range(0, self.tilesetlist[0].height):
            left = self.bresenhamLOS(self.player.relativex, self.player.relativey, 0, i, 5)
            right = self.bresenhamLOS(self.player.relativex, self.player.relativey, self.tilesetlist[0].width, i, 5)
            allpoints.append(left)
            allpoints.append(right)"""
        
        for i in self.tilesetlist[0].tilelist:
            for n in i:
                for k in allpoints:
                    for bruh in k:
                        if bruh == n.relativepos:
                            n.batch = self.tilesetlist[0].batch
                            n.visiblebyplayer = True

        for i in self.entitylist:
            for k in allpoints:
                    for bruh in k:
                        if bruh == (i.relativex, i.relativey):
                            i.batch = self.tilesetlist[0].batch
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
            points.append(current)
            """
            loop through the y and then x axis of tilelist and check if the tile is a collidable
            if it is, don't print any more points
            """
            """for i in self.tilesetlist[0].tilelist:
                for n in i:
                    if n.relativepos == current and n.collidable == True:
                        return points"""
            for i in self.tilesetlist[0].collidabletiles:
                if i.relativepos == current:
                    return points
            if D >= 0:
                y += 1
                D -= 2*dx
            D += 2*dy
        return points