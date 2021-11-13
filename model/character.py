
class Character():
    name = None
    race = None
    size = None
    str = None
    agi = None
    int = None
    hp = None
    speed = None
    perception = None
    hit = None
    critical = None
    unarmed_damage = None
    charisma = None
    pa = None
    def load_from_csv(self, csv):
        #
        self.name = csv[0]
        self.race = csv[1]
        #TODO:
        self.size = csv[2]
        #####
        self.str = csv[3]
        self.agi = csv[4]
        self.int = f'{csv[5]}'
        ####
        #TODO:
        self.hp = csv[6]
        self.speed = csv[7]
        ##
        self.perception = csv[8]
        self.hit = f'{csv[9]}' #also named acc
        self.critical = csv[10]
        #TODO:
        self.charisma = csv[11]
        self.pa = csv[12]