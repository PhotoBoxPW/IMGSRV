from PIL import Image, ImageDraw, ImageFilter
from random import randint
import numpy as np

from utils.endpoint import Endpoint, setup
from utils.perspective import autocrop


@setup
class Supreme(Endpoint):
    def generate(self, kwargs):
        text = kwargs['text']

        font = self.assets.get_font('futura.ttf', size=70)
        # this will be expanded later
        base = Image.new('RGBA', (10, 10))
        canv = ImageDraw.Draw(base)

        text_size = canv.textsize(text, font=font)

        base = Image.new('RGBA', (text_size[0] + 20, text_size[1] + 10), '#DA2727')
        canv = ImageDraw.Draw(base)

        canv.text((10, 0), text, font=font)

        return self.send_file(base)