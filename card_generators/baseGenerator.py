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

    attack_symbol = "ó"
    hex_symbol = "ę"
    ImageFile.LOAD_TRUNCATED_IMAGES = True

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
        if '{attack_symbol}' in text:
            text = text.replace('{attack_symbol}', self.attack_symbol)
        if '{hex_symbol}' in text:
            text = text.replace('{hex_symbol}', self.hex_symbol)
        return text
