from PIL import Image, ImageDraw

from utils.endpoint import Endpoint, setup
from utils.textutils import render_text_with_emoji, wrap


@setup
class Citation(Endpoint):
    def generate(self, kwargs):
        text = kwargs['text']

        if not 'header' in kwargs:
            header = 'M.O.A CITATION'
        else: header = kwargs['header']

        if not 'footer' in kwargs:
            footer = 'LAST WARNING - NO PENALTY'
        else: footer = kwargs['footer']

        base = Image.open(self.get_asset('citation.bmp')).convert('RGBA')
        font = self.assets.get_font('bmmini.ttf', size=16)
        canv = ImageDraw.Draw(base)
        text_0 = wrap(font, header, 320)
        text_1 = wrap(font, text, 320)
        canv.text((20, 10), text_0, font=font, fill='black')
        render_text_with_emoji(base, canv, (20, 45), text_1, font)
        # canv.text((20, 45), text_1, font=font)
        size = canv.textsize(footer, font=font)
        new_width = (base.width - size[0]) / 2
        canv.text((new_width, 130), footer, font=font, align='center', fill='black')

        base = base.convert('RGB')
        return self.send_file(base, format='jpeg')