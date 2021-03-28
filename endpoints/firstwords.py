from PIL import Image, ImageDraw

from utils.endpoint import Endpoint, setup
from utils.textutils import render_text_with_emoji, wrap


@setup
class FirstWords(Endpoint):
    def generate(self, kwargs):
        text = kwargs['text']

        base = Image.open(self.get_asset('firstwords.bmp'))
        font = self.assets.get_font('comic.ttf', size=55)
        canv = ImageDraw.Draw(base)
        render_text_with_emoji(base, canv, (50, 38), f"{text[0]}... {text[0]}...", font, 'black')
        render_text_with_emoji(base, canv, (30, 570), wrap(font, text, 187), font, 'black')

        base = base.convert('RGB')
        return self.send_file(base, format='jpeg')
