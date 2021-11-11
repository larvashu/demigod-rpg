import re
import textwrap
import time

from PIL import Image, ImageFont, ImageDraw, ImageFile
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches


class BaseGenerator():
    img_folder = 'resources/images/'
    desc_background_image = f'{img_folder}/card_backgrounds/desc_background.png'
    art_folder = f'{img_folder}cards/'
    output_folder = f'output/'
    tmp_file = '../tmp.png'

    y_offset = 35
    W, H = (389, 559)
    borders_start_width = 30
    borders_end_width = 327
    textures_resize_width = 213

    attack_symbol = "ó"
    hex_symbol = "ę"
    ImageFile.LOAD_TRUNCATED_IMAGES = True

    def generate(self, *args):
        pass

    def create_main_border(self, ax):
        image_borders = patches.Rectangle((0, 3), 387, 552, linewidth=3, edgecolor='black', facecolor='none')
        ax.add_patch(image_borders)
        return ax

    def create_image_borders(self, ax, y_offset):
        image_borders = patches.Rectangle((self.borders_start_width, 80+y_offset), self.borders_end_width, 207, linewidth=2, edgecolor='black', facecolor='white')
        ax.add_patch(image_borders)
        return ax

    def create_title_borders(self, ax, y_offset):
        image_borders = patches.Rectangle((self.borders_start_width, 1+ y_offset), self.borders_end_width, 67, linewidth=2, edgecolor='black', facecolor='white')
        ax.add_patch(image_borders)
        return ax

    def create_type_borders(self, ax, y_offset):
        image_borders = patches.Rectangle((self.borders_start_width, 165+ y_offset), 195, 42, linewidth=2, edgecolor='black', facecolor='none')
        ax.add_patch(image_borders)
        return ax

    def create_description_borders(self, ax, y_offset):
        image_borders = patches.Rectangle((self.borders_start_width, 310+ y_offset), self.borders_end_width, 177, linewidth=2, edgecolor='black', facecolor='white')
        ax.add_patch(image_borders)
        return ax

    def draw_action_points_cost(self, ax):
        image_borders = patches.Circle((1, 1), 65, linewidth=2, edgecolor='black', facecolor='#3776ab')
        ax.add_patch(image_borders)
        return ax

    def draw_cooldown(self, ax):
        image_borders = patches.Circle((259, 368), 65, linewidth=2, edgecolor='black', facecolor='purple')
        ax.add_patch(image_borders)
        return ax

    def write_title(self, temp_image, description):
        fontsize = 21
        #TODO: switch to python 3.10 and use match
        if len(description) > 30:
            return print('description too long, not processed (max description lenght is 24 chars)')

        if len(description) > 13:
            fontsize = 19

        if len(description) > 21:
            fontsize = 15

        if len(description) > 25:
            fontsize = 13

        font = ImageFont.truetype('resources/fonts/end.ttf',fontsize)
        draw = ImageDraw.Draw(temp_image)
        w, h = font.getsize(description)
        draw.text(((260-w)/2,(90-h)/2), description, (7, 0, 0), font=font)
        #save temp image
        temp_image.save(self.tmp_file)

    def write_type(self, temp_image, type, card_type):
        fontsize = 16
        #TODO: switch to python 3.10 and use match
        if len(card_type) > 22:
            return print('type too long, not processed (max type length is 22 chars)')

        if len(card_type) > 13:
            fontsize = 15

        if len(card_type) > 17:
            fontsize = 14

        text = f'{card_type} - {type}'
        font = ImageFont.truetype('resources/fonts/end.ttf',fontsize)
        draw = ImageDraw.Draw(temp_image)
        w, h = font.getsize(text)
        draw.text(((260-w)/2,(445-h)/2), text, (255, 255, 255), font=font, stroke_width=1, stroke_fill='black')
        #save temp image
        temp_image.save(self.tmp_file)

    def write_description(self, temp_image, description, range, aoe):
        description = self.parse_special_chars(description)
        fontsize = 12
        textwrapped = textwrap.wrap(description, width=40)
        font = ImageFont.truetype('resources/fonts/ct.ttf',fontsize)
        draw = ImageDraw.Draw(temp_image)
        w, h = font.getsize(textwrapped[0])

        if aoe:
            draw.text(((31),(265-h)), f'Range: {range}, AoE: {aoe}', (0, 0, 0), font=font)
        else:
            draw.text(((31),(265-h)), f'Range: {range}', (0, 0, 0), font=font)

        draw.text(((31),(285-h)), '\n'.join(textwrapped), (0, 0, 0), font=font)
        #save temp image
        temp_image.save(self.tmp_file)

    def write_ap_cost(self, temp_image, ap_cost):
        font = ImageFont.truetype('resources/fonts/end.ttf',46)
        draw = ImageDraw.Draw(temp_image)
        draw.text((15,-18), ap_cost, (255, 255, 255), font=font,stroke_width=1, stroke_fill='black')
        #save temp image
        temp_image.save(self.tmp_file)

    def write_cooldown_cost(self, temp_image, cd_cost):
        font = ImageFont.truetype('resources/fonts/end.ttf',46)
        draw = ImageDraw.Draw(temp_image)
        draw.text((225,295), cd_cost, (255, 255, 255), font=font,stroke_width=1, stroke_fill='black')
        #save temp image
        temp_image.save(self.tmp_file)

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
