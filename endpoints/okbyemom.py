from PIL import Image, ImageDraw

from utils import http
from utils.endpoint import Endpoint, setup
from utils.textutils import wrap, render_text_with_emoji


@setup
class Okbyemom(Endpoint):
    def generate(self, kwargs):
        text = kwargs['text']

        base = Image.open(self.get_asset('mom.bmp'))
        text_layer = Image.new('RGBA', (350, 25))
        font = self.assets.get_font('arial.ttf', size=20)
        canv = ImageDraw.Draw(text_layer)

        text = wrap(font, text, 500)

        render_text_with_emoji(text_layer, canv, (0, 0), text, font=font, fill='Black')
        text_layer = text_layer.rotate(24.75, resample=Image.BICUBIC, expand=True)

        base.paste(text_layer, (350, 443), text_layer)
        base = base.convert('RGBA')

        return self.send_file(base)