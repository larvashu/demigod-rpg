import random
from _csv import reader
from pprint import pprint

from card_generators.characterCardGenerator import CharacterGenerator

from model.character import Character

generator = CharacterGenerator()

with open('data_chars.csv', 'r') as read_obj:
    csv_reader = reader(read_obj, delimiter=",")
    next(csv_reader)
    chars = []
    results = {}
    for row in csv_reader:
        new_char = Character()
        new_char.load_from_csv(row)
        chars.append(new_char)

    for ch in chars:
        roll = random.randrange(1,20)
        zr = str(ch.zr).strip(r'\\n')
        _result = int(zr) + roll
        results[ch.name] = _result
    pprint(dict(sorted(results.items(), key=lambda item: item[1], reverse=True)), sort_dicts=False)

