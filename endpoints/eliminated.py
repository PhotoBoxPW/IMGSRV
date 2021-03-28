from PIL import Image, ImageDraw, ImageFilter
from random import randint
import numpy as np

from utils.endpoint import Endpoint, setup
from utils.perspective import autocrop


@setup
class Eliminated(Endpoint):
    def generate(self, kwargs):
        text = kwargs['text']
        num = str(randint(60, 100))
        elim_by = False if not 'elim_by' in kwargs else bool(kwargs['elim_by'])
        elim_text = 'you were eliminated by' if elim_by else 'eliminated'
        no_shadow = False if not 'no_shadow' in kwargs else bool(kwargs['no_shadow'])

        fire = Image.open(self.get_asset('fire.bmp'))
        font = self.assets.get_font('bignoodletoo.ttf', size=70)
        # this will be expanded later
        base = Image.new('RGBA', (10, 10))
        canv = ImageDraw.Draw(base)

        prefix_size = canv.textsize(elim_text, font=font)
        text_size = canv.textsize(text, font=font)
        num_size = canv.textsize(num, font=font)

        base = Image.new('RGBA', (prefix_size[0] + text_size[0] + num_size[0] + fire.width + 20, max(prefix_size[1], text_size[1], num_size[1])))
        canv = ImageDraw.Draw(base)

        canv.text((0, 0), elim_text, font=font)
        canv.text((prefix_size[0] + 10, 0), text, font=font, fill='#ff1a1a')
        if not elim_by: canv.text((prefix_size[0] + text_size[0] + 20, 0), num, font=font)

        if elim_by:
            fire = autocrop(fire)
            fire_aspect = fire.width / fire.height # lol
            fire = fire.resize((round(fire_aspect * 50), 50))
            base.paste(fire, (prefix_size[0] + text_size[0] + 20, 13), fire)
        else:
            fire_aspect = fire.width / fire.height # lol
            fire = fire.resize((round(fire_aspect * 50), 50))
            base.paste(fire, (prefix_size[0] + text_size[0] + num_size[0] + 20, 13), fire)

        base = autocrop(base)

        if not no_shadow:
            shadow_base = Image.new('RGBA', (base.width + 20, base.height + 20))
            arr = np.array(base.convert('LA'))
            arr[..., 0] = 0
            base_mask = Image.fromarray(arr, 'LA').convert('RGBA')
            shadow_base.paste(base_mask, (10, 10), base_mask)
            shadow_base = shadow_base.filter(ImageFilter.GaussianBlur(radius=5))
            shadow_base.paste(base, (10, 10), base)
            return self.send_file(shadow_base)

        return self.send_file(base)