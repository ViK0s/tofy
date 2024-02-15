import random

class Entity():
    def __init__(self, image, x, y, z, batch, group, maxhealth, atkdmg):
        self.health = maxhealth
        self.maxhealth = maxhealth
        self.atkdmg = atkdmg
        self.dead = False
    def move(self, xchange, ychange):
        self.x += xchange
        self.y += ychange 
    #this class detects colission before it happens, meaning when there's a wall before the entity, it will return true
    def detectcollision(self, tileset, xchange, ychange):
        for n in tileset:
            for i in n:
                if self.x == i.x + xchange and self.y == i.y + ychange:
                    self.checktheinteraction(i)
                    self.checkdelete()
                    return True
        return False
    #this function is made only to be overwritten, as many entities need different checks for different interactions
    def checktheinteraction(self, touched):
        pass
    def checkdelete(self):
        if self.health <= 0:
            self.dead = True
            self.__del__()
    def attack(self, other):
        other.health -= self.atkdmg
        other.checkdelete()
        print(other.health)
    def RandomizeStats(self):
        self.stats = []
        #stats in a list, starting from index 0 is str, int, wis, dex, con
        for i in range(0, 5):
            self.stats.append(random.randint(10, 20))