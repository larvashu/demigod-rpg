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
        texture_param['start_H'] = 195
        texture_param['file'] = f'{self.desc_background_image}'
        texture_param['resize_W'] = 137
        texture_param['resize_H'] = 137
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
        texture_param['start_H'] = 31
        texture_param['file'] = f'{self.desc_background_image}'
        texture_param['resize_W'] = 137
        texture_param['resize_H'] = 301
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
        texture_param['start_H'] = 31
        texture_param['file'] = f'{self.desc_background_image}'
        texture_param['resize_W'] = 137
        texture_param['resize_H'] = 301
        texture_params.append(texture_param)


        #name
        texture_param = {}
        texture_param['start_W'] = 35
        texture_param['start_H'] = 147
        texture_param['file'] = f'{self.desc_background_image}'
        texture_param['resize_W'] = 111
        texture_param['resize_H'] = 32
        texture_params.append(texture_param)
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

        self.refresh_img()
        plt.close()
        plt.savefig(f'output/champions/{char.name}', bbox_inches='tight', pad_inches=0, transparent=True)

        temp_image = Image.open(self.tmp_file)
        plt.close()

        self.refresh_img()
        plt.close()
        self.write_name_and_race(temp_image, char.name, char.race)

        self.refresh_img()

        #show and save image
        plt.savefig(f'output/skills/{char.name}', bbox_inches='tight', pad_inches=0, transparent=True)

        plt.show()


    def write_name_and_race(self, temp_image, name, race):
            fontsize = 16
            # TODO: switch to python 3.10 and use match
            if len(name) > 20:
                return print('description too long, not processed (max description lenght is 24 chars)')

            if len(name) > 13:
                fontsize = 13


            font = ImageFont.truetype('resources/fonts/end.ttf', fontsize)
            draw = ImageDraw.Draw(temp_image)
            w, h = font.getsize(name)
            draw.text(((144 - w) / 2, (325 - h) / 2), f'{name}, {race}', (7, 0, 0), font=font)
            # save temp image
            temp_image.save(self.tmp_file)

