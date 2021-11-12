import numpy as np
from PIL import Image, ImageFont, ImageDraw
import matplotlib.pyplot as plt
from card_generators.baseGenerator import BaseGenerator

char_background = "try1"
class CharacterGenerator(BaseGenerator):
    def generate(self, char):
        W, H = (1240, 877)

        im = np.array(Image.open(f'{self.img_folder}characters_backgrounds/{char_background}.png').resize((W,H)))
        fig, ax = plt.subplots()
        ax.imshow(im)

        #region borders and textures
        params = []
        texture_params =[]

        # main border
        param = {}
        param['start_W'] = 3
        param['start_H'] = 4
        param['border_W'] = W - 7
        param['border_H'] = H - 9
        param['facecolor'] = 'none'
        param['alligned'] = 0
        params.append(param)

        # portrait border
        param = {}
        param['start_W'] = 50
        param['start_H'] = 40
        param['border_W'] = 350
        param['border_H'] = 350
        param['facecolor'] = 'white'
        param['alligned'] = 35
        params.append(param)

        #portrait
        texture_param = {}
        texture_param['start_W'] = 22
        texture_param['start_H'] = 31
        texture_param['file'] = f'{self.chars_art_folder}{char.name}.jpg'
        texture_param['resize_W'] = 139
        texture_param['resize_H'] = 137
        texture_params.append(texture_param)

        # main stats
        param = {}
        param['start_W'] = 50
        param['start_H'] = 450
        param['border_W'] = 350
        param['border_H'] = 350
        param['facecolor'] = 'white'
        param['alligned'] = 35
        params.append(param)

        texture_param = {}
        texture_param['start_W'] = 22
        texture_param['start_H'] = 235
        texture_param['file'] = f'{self.desc_background_image}'
        texture_param['resize_W'] = 137
        texture_param['resize_H'] = 97
        texture_params.append(texture_param)

        # main stats_bar texture
        texture_param = {}
        texture_param['start_W'] = 22
        texture_param['start_H'] = 195
        texture_param['file'] = f'{self.chars_art_folder}char_card_bar.png'
        texture_param['resize_W'] = 137
        texture_param['resize_H'] = 37
        texture_params.append(texture_param)

        # secondary stats_bar texture
        texture_param = {}
        texture_param['start_W'] = 180
        texture_param['start_H'] = 31
        texture_param['file'] = f'{self.chars_art_folder}char_card_bar.png'
        texture_param['resize_W'] = 137
        texture_param['resize_H'] = 39
        texture_params.append(texture_param)

        # masteries texture
        texture_param = {}
        texture_param['start_W'] = 336
        texture_param['start_H'] = 31
        texture_param['file'] = f'{self.chars_art_folder}char_card_bar.png'
        texture_param['resize_W'] = 137
        texture_param['resize_H'] = 39
        texture_params.append(texture_param)


        # secondary stats
        param = {}
        param['start_W'] = 445
        param['start_H'] = 40
        param['border_W'] = 350
        param['border_H'] = 760
        param['facecolor'] = 'white'
        param['alligned'] = 35
        params.append(param)

        # secondary stats texture
        texture_param = {}
        texture_param['start_W'] = 180
        texture_param['start_H'] = 73
        texture_param['file'] = f'{self.desc_background_image}'
        texture_param['resize_W'] = 137
        texture_param['resize_H'] = 259
        texture_params.append(texture_param)

        # masteries
        param = {}
        param['start_W'] = 834
        param['start_H'] = 40
        param['border_W'] = 350
        param['border_H'] = 760
        param['facecolor'] = 'white'
        param['alligned'] = 35
        params.append(param)

        # masteries texture
        texture_param = {}
        texture_param['start_W'] = 336
        texture_param['start_H'] = 73
        texture_param['file'] = f'{self.desc_background_image}'
        texture_param['resize_W'] = 137
        texture_param['resize_H'] = 259
        texture_params.append(texture_param)


        #name
        texture_param = {}
        texture_param['start_W'] = 35
        texture_param['start_H'] = 147
        texture_param['file'] = f'{self.desc_background_image}'
        texture_param['resize_W'] = 111
        texture_param['resize_H'] = 32
        texture_params.append(texture_param)

        #main stats bar
        param = {}
        param['start_W'] = 50
        param['start_H'] = 450
        param['border_W'] = 350
        param['border_H'] = 100
        param['facecolor'] = 'none'
        param['alligned'] = 35
        params.append(param)

        #secondary stats bar
        param = {}
        param['start_W'] = 445
        param['start_H'] = 45
        param['border_W'] = 350
        param['border_H'] = 100
        param['facecolor'] = 'none'
        param['alligned'] = 35
        params.append(param)

        #masteries stats bar
        param = {}
        param['start_W'] = 834
        param['start_H'] = 45
        param['border_W'] = 350
        param['border_H'] = 100
        param['facecolor'] = 'none'
        param['alligned'] = 35
        params.append(param)


        # texture_param = {}
        # texture_param['start_W'] = 22
        # texture_param['start_H'] = 35
        # texture_param['file'] = f'{self.chars_art_folder}{char.name}.jpg'
        # texture_param['resize_W'] = 137
        # texture_param['resize_H'] = 137
        # texture_params.append(texture_param)


        #endregion

        for p in params:
            self.create_border(ax, p)
        plt.axis('off')
        plt.savefig(self.tmp_file, bbox_inches='tight', pad_inches=0, transparent=True)
        plt.close()


        temp_image = Image.open(self.tmp_file)
        for tp in texture_params:
            temp_image = self.paste_texture(temp_image, tp.get('start_W'), tp.get('start_H'), tp.get('file'),
                                            tp.get('resize_W'), tp.get('resize_H'))
        temp_image.save(self.tmp_file)

        im, fig, ax = self.refresh_img()

        # name
        param = {}
        param['start_W'] = 35
        param['start_H'] = 145
        param['border_W'] = 111
        param['border_H'] = 33
        param['facecolor'] = 'none'
        param['alligned'] = 0
        self.create_border(ax, param)
        # self.refresh_img()
        # plt.close()
        plt.savefig(self.tmp_file, bbox_inches='tight', pad_inches=0, transparent=True)

        temp_image = Image.open(self.tmp_file)
        plt.close()

        self.refresh_img()
        plt.close()
        self.write_name_and_race(temp_image, char.name, char.race)

        self.refresh_img()
        plt.close()
        self.write_main_stats_bar(temp_image, 'Main stats')

        self.refresh_img()
        plt.close()
        self.write_secondary_stats_bar(temp_image, 'Secondary')

        self.refresh_img()
        plt.close()
        self.write_masteries_bar(temp_image, 'Mastery')


        self.refresh_img()

        #show and save image
        plt.savefig(self.tmp_file, bbox_inches='tight', pad_inches=0, transparent=True)
        plt.show()
        plt.close()

        temp_image = Image.open(self.tmp_file).resize((W, H))
        temp_image.save(f'output/champions/{char.name}.png')


    def write_name_and_race(self, temp_image, name, race):
            fontsize = 17
            print(len(name)+len(race))
            # TODO: switch to python 3.10 and use match
            if len(name)+len(race) > 20:
                return print('name and race too long, not processed (max name and race length is 20 chars)')

            if len(name)+len(race) >= 13:
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
            fontsize = 21


            font = ImageFont.truetype('resources/fonts/twb.ttf', fontsize)
            draw = ImageDraw.Draw(temp_image)
            w, h = font.getsize(bar_name)
            draw.text(((178 - w) / 2, (430 - h) / 2), f'{bar_name}', (255, 255, 255), font=font ,stroke_width=1, stroke_fill='black')

            # save temp image
            temp_image.save(self.tmp_file)

    def write_secondary_stats_bar(self, temp_image, bar_name):
            fontsize = 21


            font = ImageFont.truetype('resources/fonts/twb.ttf', fontsize)
            draw = ImageDraw.Draw(temp_image)
            w, h = font.getsize(bar_name)
            draw.text(((495 - w) / 2, (106 - h) / 2), f'{bar_name}', (255, 255, 255), font=font ,stroke_width=1, stroke_fill='black')

            # save temp image
            temp_image.save(self.tmp_file)

    def write_masteries_bar(self, temp_image, bar_name):
            fontsize = 21


            font = ImageFont.truetype('resources/fonts/twb.ttf', fontsize)
            draw = ImageDraw.Draw(temp_image)
            w, h = font.getsize(bar_name)
            draw.text(((810 - w) / 2, (106 - h) / 2), f'{bar_name}', (255, 255, 255), font=font ,stroke_width=1, stroke_fill='black')

            # save temp image
            temp_image.save(self.tmp_file)
