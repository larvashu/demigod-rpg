import os
from _csv import reader
from model.skill import Skill
from card_generators.skillGenerator import SkillGenerator

generator = SkillGenerator()
with open('data.csv', 'r') as read_obj:
    csv_reader = reader(read_obj, delimiter=";")
    for row in csv_reader:
        new_skill = Skill()
        new_skill.load_from_csv(row)
        generator.generate(new_skill)

        try:
            os.remove('tmp.png')
        except:
            pass

