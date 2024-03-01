

class World():
    def __init__(self, tilesetlist, player, entitylist):
        self.tilesetlist = tilesetlist
        self.player = player
        self.entitylist = entitylist
    
    """
    a really inefficient implementation of raycasting, this will need a major rework, but it doesn't lag so it's
    fine for now?
    """
    def checkFOV(self):
        
        top = []
        down = []

        left = []
        right = []

        allpoints = []

        for i in range(0, self.tilesetlist[0].width):
            top = self.bresenhamLOS(self.player.relativex, self.player.relativey, i, self.tilesetlist[0].height)
            down = self.bresenhamLOS(self.player.relativex, self.player.relativey, i, 0)
            allpoints.append(top)
            allpoints.append(down)
 
        
        for i in range(0, self.tilesetlist[0].height):
            left = self.bresenhamLOS(self.player.relativex, self.player.relativey, 0, i)
            right = self.bresenhamLOS(self.player.relativex, self.player.relativey, self.tilesetlist[0].width, i)
            allpoints.append(left)
            allpoints.append(right)
        
        for i in self.tilesetlist[0].tilelist:
            for n in i:
                for k in allpoints:
                    for bruh in k:
                        if bruh == n.relativepos:
                            n.batch = self.tilesetlist[0].batch
        
        
                
                
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
            for i in self.tilesetlist[0].tilelist:
                for n in i:
                    if n.relativepos == current and n.collidable == True:
                        return points
            if D >= 0:
                y += 1
                D -= 2*dx
            D += 2*dy
        return points