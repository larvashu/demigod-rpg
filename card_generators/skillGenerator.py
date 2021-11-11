import os

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from card_generators.baseGenerator import BaseGenerator


class SkillGenerator(BaseGenerator):

    def generate(self, skill):
        im = np.array(Image.open(f'{self.img_folder}card_backgrounds/{skill.type}.png').resize((self.W,self.H)))
        fig, ax = plt.subplots()
        ax.imshow(im)

        # Create initial image borders
        self.create_main_border(ax)
        self.create_image_borders(ax, self.y_offset)
        self.create_title_borders(ax, self.y_offset)
        self.create_description_borders(ax, self.y_offset)
        plt.axis('off')
        plt.savefig(self.tmp_file, bbox_inches='tight', pad_inches=0, transparent=True)
        plt.close()

        #Add textures
        temp_image = Image.open(self.tmp_file)
        description_image = Image.open(self.desc_background_image).resize((self.textures_resize_width, 114))
        art = Image.open(f'{self.art_folder}{skill.art_image}.jpg').resize((self.textures_resize_width, 134))
        type_art = Image.open(f'{self.art_folder}type_back.jpg').resize((197,41))
        title_image = Image.open(self.desc_background_image).resize((self.textures_resize_width, 41))

        temp_image.paste(art, (22, 78))
        temp_image.paste(description_image, (22, 195+self.y_offset))
        temp_image.paste(title_image, (22, -9+self.y_offset))
        temp_image.paste(type_art, (30,202))
        temp_image.save(self.tmp_file)

        #refresh image
        im, fig, ax = self.refresh_img()

        #create type, ap, and cooldown borders
        self.create_type_borders(ax, self.y_offset)
        self.draw_action_points_cost(ax)
        self.draw_cooldown(ax)
        plt.savefig(self.tmp_file, bbox_inches='tight', pad_inches=0, transparent=True)
        temp_image = Image.open(self.tmp_file)
        plt.close()

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

        #show and save image
        plt.savefig(f'output/skills/{skill.title}', bbox_inches='tight', pad_inches=0, transparent=True)
        #TODO: uncomment this to show card after generated
        # plt.show()
        plt.close()
