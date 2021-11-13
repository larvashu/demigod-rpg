import numpy as np
from PIL import Image, ImageFont, ImageDraw
import matplotlib.pyplot as plt
from card_generators.baseGenerator import BaseGenerator

char_background = "try1"


class CharacterGenerator(BaseGenerator):
    def generate(self, char):
        W, H = (1240, 877)

        im = np.array(Image.open(f'{self.img_folder}characters_backgrounds/{char_background}.png').resize((W, H)))
        fig, ax = plt.subplots()
        ax.imshow(im)

        params, texture_params = self.compute_borders_and_textures(char, W, H)

        #add borders and textures layers
        for i in range(5):
            borders = []
            textures = []

            for par in params:
                if par.get('layer') == i:
                    borders.append(par)

            for tpar in texture_params:
                if tpar.get('layer') == i:
                    textures.append(tpar)

            self.add_layer(ax, borders, textures)
            im, fig, ax = self.refresh_img()

        params = self.compute_grid()
        for p in params:
            self.create_border(ax, p)

        # plt.close()
        plt.savefig(self.tmp_file, bbox_inches='tight', pad_inches=0, transparent=True)

        temp_image = Image.open(self.tmp_file)
        plt.close()

        self.refresh_img()
        plt.close()
        self.write_name_and_race(temp_image, char.name, char.race)

        self.refresh_img()
        plt.close()
        self.write_main_stats_bar(temp_image, 'Primary')

        self.refresh_img()
        plt.close()
        signs = ["Ą", "ą", "Ć"]
        self.write_sings(temp_image, signs, 80, 180, 465, 25, 15, 25)

        signs = ["ę",   "Ń"]
        self.write_sings(temp_image,signs, 387, 455, 160, 25, 14, 22)

        signs = ["Ę","ć", ]
        self.write_sings(temp_image,signs, 387, 455, 160+150, 25, 14, 22)

        signs = ["ł", "Ł", "ń" ]
        self.write_sings(temp_image,signs, 387, 455, 160+300, 25, 14, 22)

        self.refresh_img()
        plt.close()
        self.write_secondary_stats_text_and_bar(temp_image, 'Secondary')

        self.refresh_img()
        plt.close()
        self.write_masteries_bar(temp_image, 'Masteries')

        self.refresh_img()

        # show and save image
        plt.savefig(self.tmp_file, bbox_inches='tight', pad_inches=0, transparent=True)
        plt.show()
        plt.close()

        temp_image = Image.open(self.tmp_file).resize((W, H))
        temp_image.save(f'output/champions/{char.name}.png')

    def write_name_and_race(self, temp_image, name, race):
        fontsize = 17
        # TODO: switch to python 3.10 and use match
        if len(name) + len(race) > 20:
            return print('name and race too long, not processed (max name and race length is 20 chars)')

        if len(name) + len(race) >= 13:
            fontsize = 13

        font = ImageFont.truetype('resources/fonts/end.ttf', fontsize)
        draw = ImageDraw.Draw(temp_image)
        w, h = font.getsize(name)
        if race:
            draw.text(((128 - w) / 2, (325 - h) / 2), f'{name}, {race}', (7, 0, 0), font=font)
        else:
            draw.text(((128 - w) / 2, (325 - h) / 2), f'{name}', (7, 0, 0), font=font)

        # save temp image
        temp_image.save(self.tmp_file)

    def write_main_stats_bar(self, temp_image, bar_name):
        fontsize = 24

        font = ImageFont.truetype('resources/fonts/twb.ttf', fontsize)
        draw = ImageDraw.Draw(temp_image)
        w, h = font.getsize(bar_name)
        draw.text(((178 - w) / 2, (430 - h) / 2), f'{bar_name}', (255, 255, 255), font=font, stroke_width=1,
                  stroke_fill='black')

        # save temp image
        temp_image.save(self.tmp_file)

    def write_secondary_stats_text_and_bar(self, temp_image, bar_name):
        fontsize = 21

        font = ImageFont.truetype('resources/fonts/twb.ttf', fontsize)
        draw = ImageDraw.Draw(temp_image)
        w, h = font.getsize(bar_name)
        draw.text(((495 - w) / 2, (106 - h) / 2), f'{bar_name}', (255, 255, 255), font=font, stroke_width=1,
                  stroke_fill='black')

        fontsize = 12
        font = ImageFont.truetype('resources/fonts/twb.ttf', fontsize)
        w, h = font.getsize('Base')
        draw.text(((532 - w) / 2, (169 - h) / 2), f'Base', (55, 55, 55), font=font)

        fontsize = 12
        font = ImageFont.truetype('resources/fonts/twb.ttf', fontsize)
        w, h = font.getsize('Bonus')
        draw.text(((597 - w) / 2, (169 - h) / 2), f'Bonus', (55, 55, 55), font=font)

        fontsize = 12
        font = ImageFont.truetype('resources/fonts/twb.ttf', fontsize)
        w, h = font.getsize('Base')
        for i in range(119):
            draw.text(((392 - w) / 2+i, (310 - h) / 2), f'-', (0, 0, 0), font=font)

        fontsize = 12
        font = ImageFont.truetype('resources/fonts/twb.ttf', fontsize)
        w, h = font.getsize('Base')
        for i in range(119):
            draw.text(((392 - w) / 2+i, (460 - h) / 2), f'-', (0, 0, 0), font=font)


        # save temp image
        temp_image.save(self.tmp_file)

    def write_masteries_bar(self, temp_image, bar_name):
        fontsize = 21

        font = ImageFont.truetype('resources/fonts/twb.ttf', fontsize)
        draw = ImageDraw.Draw(temp_image)
        w, h = font.getsize(bar_name)
        draw.text(((810 - w) / 2, (106 - h) / 2), f'{bar_name}', (255, 255, 255), font=font, stroke_width=1,
                  stroke_fill='black')

        # save temp image
        temp_image.save(self.tmp_file)

    def write_sings(self, temp_image, signs,text_w_start, w_start,x_start,space,sign_size,font_size):

        draw = ImageDraw.Draw(temp_image)

        i = 0
        for sign in signs:
            fontsize = font_size
            font = ImageFont.truetype('resources/fonts/twb.ttf', fontsize)
            i += 1
            w, h = font.getsize(sign)
            draw.text(((text_w_start - w) / 2, ((x_start - h) / 2) + i*space), f'{sign}', (255, 255, 255), font=font, stroke_width=1,stroke_fill='black')

            if sign == "Ą":
                fontsize = sign_size
                font = ImageFont.truetype('resources/fonts/twb.ttf', fontsize)
                w, h = font.getsize('Strength')
                draw.text(((w_start - w) / 2, ((x_start - h) / 2) + i * space), f'Strength', (55, 55, 55), font=font)

            if sign == "ą":
                fontsize = sign_size
                font = ImageFont.truetype('resources/fonts/twb.ttf', fontsize)
                w, h = font.getsize('Agility')
                draw.text(((w_start - w) / 2, ((x_start - h) / 2) + i * space), f'Agility', (55, 55, 55), font=font)

            if sign == "Ć":
                fontsize = sign_size
                font = ImageFont.truetype('resources/fonts/twb.ttf', fontsize)
                w, h = font.getsize('Intelligence')
                draw.text(((w_start - w) / 2, ((x_start - h) / 2) + i * space), f'Intelligence', (55, 55, 55), font=font)

            if sign == "ć":
                fontsize = sign_size
                font = ImageFont.truetype('resources/fonts/twb.ttf', fontsize)
                w, h = font.getsize('Crit')
                draw.text(((w_start - w-7) / 2, ((x_start - h) / 2) + i * space), f'Critic', (5, 5, 5), font=font)

            if sign == "Ę":
                fontsize = 11
                font = ImageFont.truetype('resources/fonts/twb.ttf', fontsize)
                w, h = font.getsize('Accuracy')
                draw.text(((w_start - w+6) / 2, ((x_start - h) / 2) + i * space), f'Accuracy', (5, 5, 5), font=font)

            if sign == "ę":
                fontsize = 10
                font = ImageFont.truetype('resources/fonts/twb.ttf', fontsize)
                w, h = font.getsize('Perception')
                draw.text(((w_start - w+5) / 2, ((x_start - h) / 2) + i * space), f'Perception', (5, 5, 5), font=font)

            if sign == "Ł":
                fontsize = 12
                font = ImageFont.truetype('resources/fonts/twb.ttf', fontsize)
                w, h = font.getsize('Speed')
                draw.text(((w_start - w+5) / 2, ((x_start - h) / 2) + i * space), f'Speed', (5, 5, 5), font=font)

            if sign == "Ń":
                fontsize = 10
                font = ImageFont.truetype('resources/fonts/twb.ttf', fontsize)
                w, h = font.getsize('Charisma')
                draw.text(((w_start - w+5) / 2, ((x_start - h) / 2) + i * space), f'Charisma', (5, 5, 5), font=font)

            if sign == "ł":
                fontsize = 12
                font = ImageFont.truetype('resources/fonts/twb.ttf', fontsize)
                w, h = font.getsize('HP')
                draw.text(((w_start - w+5) / 2, ((x_start - h) / 2) + i * space), f'HP', (5, 5, 5), font=font)

            if sign == "ń":
                fontsize = 12
                font = ImageFont.truetype('resources/fonts/twb.ttf', fontsize)
                w, h = font.getsize('Actions')
                draw.text(((w_start - w+5) / 2, ((x_start - h) / 2) + i * space), f'Actions', (5, 5, 5), font=font)


        # save temp image
        temp_image.save(self.tmp_file)

        # main border

    def compute_borders_and_textures(self, char, W, H):
            dic = {}
            #main frame
            dic["border_main"] = [3,4,W-7,H-9,'none',0,0]

            #portrait
            dic["border_portrait"] = [50, 40, 350, 350, 'white', 35, 0]
            dic["texture_portrait"] = [22,31,f'{self.chars_art_folder}{char.name}.jpg', 139, 137,0]

            #main stats
            dic["border_main_stats"] = [50,450,350,350,'white', 35, 0]
            dic["texture_main_stats"] = [22,235, f'{self.desc_background_image}', 137, 97,0]
            dic["texture_main_stats_bar"] = [22,195,f'{self.chars_art_folder}char_card_bar.png', 137, 37,0]
            dic["border_ms_bar"] = [50,450,350,100,'none',35,0]

            #secondary stats
            dic["border_secondary_stats"] = [445,40,350,760,'white',35,0]
            dic["texture_secondary_bar"] = [180,31,f'{self.chars_art_folder}char_card_bar.png',137, 39,0]
            dic["texture_secondary_stats"] = [180,73,f'{self.desc_background_image}', 137,259,0]
            dic["border_ss_bar"] = [445,45,350,100, 'none',35,0]

            #masteries
            dic["texture_masteries_bar"] = [336, 31, f'{self.chars_art_folder}char_card_bar.png', 137,39,0]
            dic["border_masteries"] = [834,40,350,760,'white',35,0]
            dic["texture_masteries"] = [336,73,f'{self.desc_background_image}', 137,259,0]
            dic["border_m_bar"] = [834,45,350,100,'none',35,0]

            #name
            dic["texture_name"] = [35,147,f'{self.desc_background_image}', 111, 32,0]
            dic["border_name"] = [35,145,111,33,'none',0,1]

            borders = []
            textures = []
            for item in dic:
                if "texture" in item:
                    textures.append(item)
                if "border" in item:
                    borders.append(item)

            params = []
            texture_params = []

            for item in borders:
                param = {}
                param['start_W'] = dic[item][0]
                param['start_H'] = dic[item][1]
                param['border_W'] = dic[item][2]
                param['border_H'] = dic[item][3]
                param['facecolor'] = dic[item][4]
                param['alligned'] = dic[item][5]
                param['layer'] = dic[item][6]
                params.append(param)

            for item in textures:
                texture_param = {}
                texture_param['start_W'] = dic[item][0]
                texture_param['start_H'] = dic[item][1]
                texture_param['file'] = dic[item][2]
                texture_param['resize_W'] = dic[item][3]
                texture_param['resize_H'] = dic[item][4]
                texture_param['layer'] = dic[item][5]
                texture_params.append(texture_param)
            return params, texture_params

    def compute_grid(self):
        dic = {}
        params = []
        #main stats
        for i in range(3):
            dic[f"border_secondary_main_stats_{i}"] = [129, 210 + i * 25, 20, 20, 'white', 35, 0]

        #secondary stats_stats
        for j in range(3):
            for i in range(2):
                dic[f"border_secondary_bonus_stats_{j}-{i}"] = [255, 60+75*j + i * 25, 20, 20, 'white', 35, 0]

            for i in range(2):
                dic[f"border_secondary_total_stats_{j}-{i}"] = [285, 60+75*j + i * 25, 20, 20, 'white', 35, 0]

        dic[f"border_secondary_bonus_stats_-1"] = [255, 60+75 + 5 * 25, 20, 20, 'white', 35, 0]
        dic[f"border_secondary_bonus_stats_-2"] = [285, 60+75 + 5 * 25, 20, 20, 'white', 35, 0]

        # for i in range(2):
        #     dic[f"border_secondary_bonus_stats_{i}"] = [255, 110 + i * 25, 20, 20, 'white', 35, 0]
        #
        # for i in range(2):
        #     dic[f"border_secondary_total_stats_{i}"] = [285, 110 + i * 25, 20, 20, 'white', 35, 0]


        for item in dic:
                param = {}
                param['start_W'] = dic[item][0]
                param['start_H'] = dic[item][1]
                param['border_W'] = dic[item][2]
                param['border_H'] = dic[item][3]
                param['facecolor'] = dic[item][4]
                param['alligned'] = dic[item][5]
                param['layer'] = dic[item][6]
                params.append(param)

        return params

    def add_layer(self, ax, params, texture_params):
        #draw borders
        for p in params:
            self.create_border(ax, p)
        plt.axis('off')
        plt.savefig(self.tmp_file, bbox_inches='tight', pad_inches=0, transparent=True)
        plt.close()

        #paste textures
        temp_image = Image.open(self.tmp_file)
        for tp in texture_params:
            temp_image = self.paste_texture(temp_image, tp.get('start_W'), tp.get('start_H'), tp.get('file'),
                                            tp.get('resize_W'), tp.get('resize_H'))
        temp_image.save(self.tmp_file)

