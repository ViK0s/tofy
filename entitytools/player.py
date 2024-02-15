import entity

class Player(entity.Entity):
    def __init__(self, image, x, y, z, batch, group, maxhealth,atkdmg):
        super().__init__(image, x, y, z,  batch, group, maxhealth, atkdmg)
        self.RandomizeStats()
        self.maxhealth += self.stats[4]
        self.health = self.maxhealth
        self.pickeditems = []
        self.poisoned = False
        atkdmg += self.stats[0]
        self.atkdmgbase = atkdmg
        self.level = 1
        self.win = False
    def attack(self, other):
        other.health -= self.atkdmg
        other.checkdelete()
    def pickup(self, other):
        bruh = -1
        for i in other.stats:
            bruh += 1
            if i > self.stats[bruh]:
                print("can't pick the item because you don't have the stats")
                return
        #this is a hack, all items have nearly 0 hp, so they "die" when picked up
        self.attack(other)
        self.pickeditems.append(other)
        print(self.pickeditems)
    def addcontrols():
        pass