from docx import Document
from docx.shared import Cm
from PIL import Image

import glob
for item in glob.glob("output/skills/*"):
    picture = Image.open(item)
    s = item[item.index('\\'):].replace('\\', '')
    picture.rotate(90,expand=1).save(f'output/rotated/{s}')

document = Document()

sections = document.sections
for section in sections:
    section.top_margin = Cm(0.5)
    section.bottom_margin = Cm(0.5)
    section.left_margin = Cm(0.5)
    section.right_margin = Cm(0.5)

for img in glob.glob("output/rotated/*"):
    document.add_picture(img, width=Cm(8.8))

document.save('out.docx')


