import os
import textwrap
import time

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageFont, ImageDraw
from matplotlib import patches
from card_generators.baseGenerator import BaseGenerator


class CharacterGenerator(BaseGenerator):

    def generate(self, character):
        W, H = (389, 559)
        params = []
        texture_params = []

        # params for aligned borders
        borders_start_width = 30
        borders_end_width = 327
        textures_resize_width = 213

        # region border_params

        # main border
        param = {}
        param['start_W'] = 1
        param['start_H'] = 4
        param['border_W'] = W - 6
        param['border_H'] = H - 7
        param['facecolor'] = 'none'
        param['alligned'] = 0
        params.append(param)

        # title
        param = {}
        param['start_W'] = borders_start_width
        param['start_H'] = 37
        param['border_W'] = borders_end_width
        param['border_H'] = 67
        param['facecolor'] = 'white'
        param['alligned'] = 0
        params.append(param)

        texture_param = {}
        texture_param['start_W'] = 22
        texture_param['start_H'] = -9 + self.y_offset
        texture_param['file'] =  f'{self.skills_art_folder}type_back.jpg'
        texture_param['resize_W'] = textures_resize_width
        texture_param['resize_H'] = 41
        texture_params.append(texture_param)

        # description
        param = {}
        param['start_W'] = borders_start_width
        param['start_H'] = 100
        param['border_W'] = borders_end_width
        param['border_H'] = 390
        param['facecolor'] = 'white'
        param['alligned'] = 35
        params.append(param)

        texture_param = {}
        texture_param['start_W'] = 22
        texture_param['start_H'] = 55+self.y_offset
        texture_param['file'] = self.desc_background_image
        texture_param['resize_W'] = textures_resize_width
        texture_param['resize_H'] = 256
        params.append(param)
        texture_params.append(texture_param)


        #endregion

        im = np.array(Image.open(f'{self.img_folder}card_backgrounds/{character.type}.png').resize((W,H)))
        fig, ax = plt.subplots()
        ax.imshow(im)

        for p in params:
            self.create_border(ax, p)
        plt.axis('off')
        plt.savefig(self.tmp_file, bbox_inches='tight', pad_inches=0, transparent=True)
        plt.close()

        #Add textures
        temp_image = Image.open(self.tmp_file)
        for tp in texture_params:
            temp_image = self.paste_texture(temp_image, tp.get('start_W'), tp.get('start_H'), tp.get('file'), tp.get('resize_W'), tp.get('resize_H'))
        temp_image.save(self.tmp_file)

        #refresh image
        im, fig, ax = self.refresh_img()

        #region write data on cards
        #add title
        self.refresh_img()
        plt.close()
        self.write_title(temp_image, character.name)

        #add type
        self.refresh_img()
        plt.close()
        self.write_description(temp_image, character)


        #refresh image
        self.refresh_img()
        #endregion

        #show and save image
        plt.savefig(f'output/skills/{character.name}', bbox_inches='tight', pad_inches=0, transparent=True)
        #TODO: uncomment this to show card after generated
        # plt.show()
        plt.close()

        #resize
        temp_image = Image.open(self.tmp_file).resize((389, 559))
        print('here')
        #makedir
        dir = (f'output/chars/')
        if not os.path.isdir(dir):
            os.mkdir(dir)
        temp_image.save(f'{dir}/{character.name}.png')


    #drawing skill methods
    def draw_cooldown(self, ax):
        image_borders = patches.Circle((258, 367), 65, linewidth=2, edgecolor='black', facecolor='purple')
        ax.add_patch(image_borders)
        return ax
    def draw_armor(self, ax):
        image_borders = patches.Circle((258, 367), 65, linewidth=2, edgecolor='black', facecolor='gray')
        ax.add_patch(image_borders)
        return ax

    def draw_compation_hp(self, ax):
        image_borders = patches.Circle((258, 367), 65, linewidth=2, edgecolor='black', facecolor='red')
        ax.add_patch(image_borders)
        return ax


    def write_cooldown_cost(self, temp_image, cd_cost):
        font = ImageFont.truetype('resources/fonts/twb.ttf',57)
        draw = ImageDraw.Draw(temp_image)
        draw.text((220,313), cd_cost, (255, 255, 255), font=font,stroke_width=1, stroke_fill='black')
        #save temp image
        temp_image.save(self.tmp_file)

    def draw_action_points_cost(self, ax):
        image_borders = patches.Circle((-9, 7), 65, linewidth=2, edgecolor='black', facecolor='#3776ab')
        ax.add_patch(image_borders)
        return ax

    def draw_attack(self, ax):
        image_borders = patches.Circle((-9, 7), 65, linewidth=2, edgecolor='black', facecolor='gray')
        ax.add_patch(image_borders)
        return ax

    #writing data methods
    def write_ap_cost(self, temp_image, ap_cost):
        font = ImageFont.truetype('resources/fonts/twb.ttf',57)
        draw = ImageDraw.Draw(temp_image)
        if ap_cost == "1":
            draw.text((12, -2), ap_cost, (255, 255, 255), font=font, stroke_width=1, stroke_fill='black')
        else:
            draw.text((7,-2), ap_cost, (255, 255, 255), font=font,stroke_width=1, stroke_fill='black')
        #save temp image
        temp_image.save(self.tmp_file)

    def write_description(self, temp_image, character):
        nominal_width = 35
        description = \
            f'(PZ)  Punkty Zycia: {character.hp}' \
            f'(A)   Akcje: {character.akcje}' \
            f'(Sz)  Szybkosc: {character.szybkosc}' \
            f'(S)   Sila: {character.sila}' \
            f'(Mag) Magia: {character.mag}' \
            f'(WW)  Walka wrecz: {character.ww}' \
            f'(US)  Um. strzeleckie: {character.us}' \
            f'(K)   Krzepa: {character.k}' \
            f'(Odp) Odpornosc: {character.odp}' \
            f'(Zr)  Zrecznosc: {character.zr}' \
            f'(Sw)  Sila Woli: {character.sw}' \
            f'(Ogl) Oglada: {character.ogl}'

        print(description)
        description = self.parse_special_chars(description)

        description, spec_char_pos = self.parse_newlines(description, nominal_width)

        print(description)
        print(spec_char_pos)

        fontsize = 22
        multiplier = 1.07
        _rangeMultiplier = 1.10
        textwrapped = textwrap.wrap(description, width=35, replace_whitespace=False, drop_whitespace=False)
        if len(textwrapped) > 4:
            multiplier = 1.08
            _rangeMultiplier = 1.11
            fontsize = 13
        font = ImageFont.truetype('resources/fonts/ct.ttf', fontsize)
        draw = ImageDraw.Draw(temp_image)
        w, h = font.getsize(textwrapped[0])

        draw.text(((31),(115-h)), '\n'.join(textwrapped), (0, 0, 0), font=font)

        i = 0
        for line in textwrapped:
            print(f"line: {line}")
            for special_char_p in spec_char_pos:
                if special_char_p['line_nr'] == i:
                    for indic in special_char_p['indices']:
                        if special_char_p['special_char'] == self.cd_symbol:
                            try:
                                prefix = line[0:indic]
                                print(f'prefix: {prefix}')
                                w,_h = font.getsize(prefix)
                                # h = 15
                                print(f'w, h: {w, h}')
                                string = special_char_p['special_char']
                                print(string)
                                draw.text(((31 + w), (hs - h + (h * i * multiplier))), string, (147, 0, 150), font=font, stroke_width=1, stroke_fill='black')
                            except:
                                print('no trudno')

                        if special_char_p['special_char'] == self.ap_symbol:
                                try:
                                    prefix = line[0:indic]
                                    w, _h = font.getsize(prefix)
                                    string = special_char_p['special_char']
                                    print(string)
                                    hs = 285
                                    draw.text(((31 + w), (hs - h + (h * i * multiplier))), string, (0,191,255), font=font,
                                              stroke_width=1, stroke_fill='black')

                                except:
                                    print('no trudno')

                        if special_char_p['special_char'] == self.charge_symbol:
                                try:
                                    prefix = line[0:indic]
                                    print(f'prefix 2: {prefix}')
                                    w, _h = font.getsize(prefix)
                                    # h = 15
                                    print(f'w, h: {w, h}')
                                    string = special_char_p['special_char']
                                    print(string)
                                    hs = 285
                                    draw.text(((31 + w), (hs - h + (h * i * multiplier))), string, (50,205,50), font=font,
                                              stroke_width=1, stroke_fill='black')

                                except:
                                    print('no trudno')

                        if special_char_p['special_char'] == self.hp_symbol:
                                print('hehe')
                                try:
                                    prefix = line[0:indic]
                                    print(f'prefix: {prefix}')
                                    w, h = font.getsize(prefix)
                                    h = 16
                                    print(f'w, h: {w, h}')
                                    string = special_char_p['special_char']
                                    print(string)
                                    hs = 285
                                    draw.text(((31 + w), (hs - h + (h * i * multiplier))), string, (255,69,0), font=font,
                                              stroke_width=1, stroke_fill='black')

                                except:
                                    print('no trudno')
            i += 1


            # draw.text()
        #save temp image
        temp_image.save(self.tmp_file)
    def write_type(self, temp_image, type, card_type):
        fontsize = 22
        #TODO: switch to python 3.10 and use match
        if len(card_type) > 22:
            return print('type too long, not processed (max type length is 22 chars)')

        if len(card_type) > 13:
            fontsize = 20

        if len(card_type) > 17:
            fontsize = 18

        text = f'{card_type}'
        font = ImageFont.truetype('resources/fonts/twb.ttf',fontsize)
        draw = ImageDraw.Draw(temp_image)
        w, h = font.getsize(text)
        draw.text(((260-w)/2,(445-h)/2), text, (255, 255, 255), font=font, stroke_width=1, stroke_fill='black')
        #save temp image
        temp_image.save(self.tmp_file)

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
