#type, art_image, description, ap_cost, cd_cost, card_type, card_text, range, aoe

class Skill():
    type = None
    art_image = None
    title = None
    ap_cost = None
    cd_cost = None
    card_type = None
    card_text = None
    range = None
    aoe = None

    def load_from_csv(self, csv):
        self.art_image = csv[0]
        self.title = csv[0]
        self.type=csv[1]
        self.ap_cost = csv[2]
        self.cd_cost = csv[3]
        self.card_type = f'{csv[4]}'
        self.card_text = csv[5]
        self.range = csv[6]
        self.aoe = csv[7]

    # def __init__(self):
    #     pass