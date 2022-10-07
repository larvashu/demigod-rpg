
class Character():
    name = None

    akcje = None
    hp = None
    sila = None
    szybkosc = None

    ww = None
    us = None
    k = None
    odp = None
    zr = None
    sw = None
    ogl = None
    mag = None

    type = None
    def load_from_csv(self, csv):
        self.name = csv[0]
        self.akcje = csv[1]
        self.hp = csv[2]
        self.sila = csv[3]
        self.szybkosc = csv[4]
        self.ww = csv[5]
        self.us = csv[6]
        self.k = csv[7]
        self.odp = csv[8]
        self.zr = csv[9]
        self.sw = csv[10]
        self.ogl = csv[11]
        self.type = csv[12]
        self.mag = csv[13]