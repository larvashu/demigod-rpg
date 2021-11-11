import textwrap
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageFont, ImageDraw
from matplotlib import patches
from card_generators.baseGenerator import BaseGenerator


class SkillGenerator(BaseGenerator):

    def generate(self, skill):
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

        # image
        param = {}
        param['start_W'] = borders_start_width
        param['start_H'] = 80
        param['border_W'] = borders_end_width
        param['border_H'] = 207
        param['facecolor'] = 'white'
        param['alligned'] = 35
        params.append(param)

        texture_param = {}
        texture_param['start_W'] = 22
        texture_param['start_H'] = 78
        texture_param['file'] = f'{self.art_folder}{skill.art_image}.jpg'
        texture_param['resize_W'] = textures_resize_width
        texture_param['resize_H'] = 134
        texture_params.append(texture_param)

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
        texture_param['file'] =  f'{self.art_folder}type_back.jpg'
        texture_param['resize_W'] = textures_resize_width
        texture_param['resize_H'] = 41
        texture_params.append(texture_param)

        # description
        param = {}
        param['start_W'] = borders_start_width
        param['start_H'] = 310
        param['border_W'] = borders_end_width
        param['border_H'] = 177
        param['facecolor'] = 'white'
        param['alligned'] = 35
        params.append(param)

        texture_param = {}
        texture_param['start_W'] = 22
        texture_param['start_H'] = 195+self.y_offset
        texture_param['file'] = self.desc_background_image
        texture_param['resize_W'] = textures_resize_width
        texture_param['resize_H'] = 114
        params.append(param)
        texture_params.append(texture_param)

        # type
        param = {}
        param['start_W'] = borders_start_width
        param['start_H'] = 165
        param['border_W'] = 197
        param['border_H'] = 42
        param['facecolor'] = 'none'
        param['alligned'] = 35
        params.append(param)

        texture_param = {}
        texture_param['start_W'] = 30
        texture_param['start_H'] = 202
        texture_param['file'] =  f'{self.art_folder}type_back.jpg'
        texture_param['resize_W'] = 197
        texture_param['resize_H'] = 41
        texture_params.append(texture_param)

        #endregion

        im = np.array(Image.open(f'{self.img_folder}card_backgrounds/{skill.type}.png').resize((W,H)))
        fig, ax = plt.subplots()
        ax.imshow(im)

        for p in params:
            self.create_border(ax, p.get('start_W'), p.get('start_H'), p.get('border_W'), p.get('border_H'), p.get('alligned'), p.get('facecolor'))
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

        #create type, ap, and cooldown borders
        p = params[5]
        self.create_border(ax, p.get('start_W'), p.get('start_H'), p.get('border_W'), p.get('border_H'), p.get('alligned'), p.get('facecolor'))
        self.draw_action_points_cost(ax)
        self.draw_cooldown(ax)

        plt.savefig(self.tmp_file, bbox_inches='tight', pad_inches=0, transparent=True)
        temp_image = Image.open(self.tmp_file)
        plt.close()

        #region write data on cards
        #add title
        self.refresh_img()
        plt.close()
        self.write_title(temp_image, skill.title)

        #add type
        self.refresh_img()
        plt.close()
        self.write_type(temp_image, skill.type, skill.card_type)

        #add type
        self.refresh_img()
        plt.close()
        self.write_description(temp_image, skill.card_text, skill.range, skill.aoe)

        #add ap cost
        self.refresh_img()
        plt.close()
        self.write_ap_cost(temp_image, skill.ap_cost)

        #add cooldown cost
        self.refresh_img()
        plt.close()
        self.write_cooldown_cost(temp_image, skill.cd_cost)

        #refresh image
        self.refresh_img()
        #endregion

        #show and save image
        plt.savefig(f'output/skills/{skill.title}', bbox_inches='tight', pad_inches=0, transparent=True)
        #TODO: uncomment this to show card after generated
        # plt.show()
        plt.close()

        #resize
        temp_image = Image.open(self.tmp_file).resize((389, 559))
        temp_image.save(f'output/skills/{skill.title}.png')

    #drawing skill methods
    def draw_cooldown(self, ax):
        image_borders = patches.Circle((259, 368), 65, linewidth=2, edgecolor='black', facecolor='purple')
        ax.add_patch(image_borders)
        return ax

    def write_cooldown_cost(self, temp_image, cd_cost):
        font = ImageFont.truetype('resources/fonts/end.ttf',46)
        draw = ImageDraw.Draw(temp_image)
        draw.text((225,295), cd_cost, (255, 255, 255), font=font,stroke_width=1, stroke_fill='black')
        #save temp image
        temp_image.save(self.tmp_file)

    def draw_action_points_cost(self, ax):
        image_borders = patches.Circle((1, 1), 65, linewidth=2, edgecolor='black', facecolor='#3776ab')
        ax.add_patch(image_borders)
        return ax

    #writing data methods
    def write_ap_cost(self, temp_image, ap_cost):
        font = ImageFont.truetype('resources/fonts/end.ttf',46)
        draw = ImageDraw.Draw(temp_image)
        draw.text((15,-18), ap_cost, (255, 255, 255), font=font,stroke_width=1, stroke_fill='black')
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
