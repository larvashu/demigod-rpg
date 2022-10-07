import os
import sys
from _csv import reader

from model.character import Character
from model.skill import Skill
from card_generators.skillGenerator import SkillGenerator
from card_generators.characterCardGenerator import CharacterGenerator

type = "character"

if type == "skill":
        generator = SkillGenerator()
        with open(f'data_saju.csv', 'r') as read_obj:
            csv_reader = reader(read_obj, delimiter=";")
            for row in csv_reader:
                new_skill = Skill()
                new_skill.load_from_csv(row)
                generator.generate(new_skill)
                try:
                    os.remove('tmp.png')
                except:
                    pass


if type == "skill":
    dir = f"./resources/cards_definition/"
    all_files = os.listdir(dir)
    csv_files = list(filter(lambda f: f.endswith('.csv'), all_files))

    for file in csv_files:
        generator = SkillGenerator()
        with open(f'{dir}{file}', 'r') as read_obj:
            csv_reader = reader(read_obj, delimiter=";")
            for row in csv_reader:
                new_skill = Skill()
                new_skill.load_from_csv(row)
                generator.generate(new_skill)
                try:
                    os.remove('tmp.png')
                except:
                    pass

if type == "character":
    generator = CharacterGenerator()
    print(generator)
    with open('data_chars.csv', 'r') as read_obj:
        csv_reader = reader(read_obj, delimiter=",")
        next(csv_reader)
        for row in csv_reader:
            new_char = Character()
            new_char.load_from_csv(row)
            generator.generate(new_char)
            try:
                os.remove('tmp.png')
            except:
                pass
