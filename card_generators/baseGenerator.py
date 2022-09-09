import textwrap

import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageFile


class BaseGenerator():

    img_folder = 'resources/images/'
    desc_background_image = f'{img_folder}card_backgrounds/desc_background.png'
    skills_art_folder = f'{img_folder}cards/'
    chars_art_folder = f'{img_folder}characters/'
    output_folder = f'output/'
    tmp_file = '../tmp.png'

    y_offset = 35
    borders_start_width = None
    borders_start_h = None
    textures_resize_width = None

    hp_symbol = "^"
    ap_symbol = "ó"
    hex_symbol = "ę"
    cd_symbol = "ą"
    roll_symbol = "ż"
    damage_symbol = "#"
    armor_symbol = "&"
    ImageFile.LOAD_TRUNCATED_IMAGES = True

    special_chars_pos = []

    def generate(self, *args):
        pass

    def create_border(self, ax, p):
        image_borders = patches.Rectangle((p.get('start_W'), p.get('start_H')+p.get('alligned')), p.get('border_W'), p.get('border_H'), linewidth=2, edgecolor='black', facecolor=p.get('facecolor'))
        ax.add_patch(image_borders)
        return ax


    def paste_texture(self, temp_image, texture_start_w, texture_start_h, file, width, height):
        img = Image.open(file).resize((width, height))
        temp_image.paste(img, (texture_start_w, texture_start_h))
        return temp_image

    def refresh_img(self):
        im = np.array(Image.open(self.tmp_file))
        fig, ax = plt.subplots()
        ax.imshow(im)
        plt.axis('off')
        return im, fig, ax

    def parse_special_chars(self, text):
        ##TODO: this is ugly
        if '{armor_symbol}' in text:
            text = text.replace('{armor_symbol}', self.armor_symbol)
        if '{hp_symbol}' in text:
            text = text.replace('{hp_symbol}', self.hp_symbol)
        if '{ap_symbol}' in text:
            text = text.replace('{ap_symbol}', self.ap_symbol)
        if '{hex_symbol}' in text:
            text = text.replace('{hex_symbol}', self.hex_symbol)
        if '{cd_symbol}' in text:
            text = text.replace('{cd_symbol}', self.cd_symbol)
        if '{roll_symbol}' in text:
            text = text.replace('{roll_symbol}', self.roll_symbol)
        if '{damage_symbol}' in text:
            text = text.replace('{damage_symbol}', self.damage_symbol)

        return text

    def parse_newlines(self, text, nominal_width):
        results = []
        special_char_pos = []
        _copy = text
        newline_sign = r'\n'
        while text:
            _textwrapped = textwrap.wrap(text, width=35, replace_whitespace=False, drop_whitespace=False)
            for wrap in _textwrapped:
                if newline_sign in wrap:
                    value = wrap
                    res = value[:value.index(newline_sign)+len(newline_sign)]
                    fill = nominal_width - len(res)
                    for i in range(fill):
                        res += ' '
                    res = res.replace(r'\n', ' ')
                    results.append(res)
                    break
                else:
                    results.append(wrap)
            text = text[text.index(newline_sign)+len(newline_sign):]
        _copy = 0
        specials = [self.cd_symbol, self.ap_symbol, self.hex_symbol, self.hp_symbol]

        line_nr = 0
        for line in results:
            for sp in specials:
                if sp in line:
                    indices = [i for i, x in enumerate(line) if x == sp]
                    special_char_pos.append({
                        'line_nr': line_nr,
                        'special_char': sp,
                        'indices': indices
                    })
            line_nr += 1
        result_string = "".join(results)
        return result_string, special_char_pos

