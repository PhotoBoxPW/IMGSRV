from PIL import Image, ImageDraw

from utils.endpoint import Endpoint, setup
from utils.textutils import render_text_with_emoji, wrap


@setup
class Clippy(Endpoint):
    def generate(self, kwargs):
        text = kwargs['text']

        base = Image.open(self.get_asset('clippy.bmp'))
        font = self.assets.get_font('arial.ttf', size=20)
        canv = ImageDraw.Draw(base)
        render_text_with_emoji(base, canv, (28, 36), wrap(font, text, 290), font, 'black')

        return self.send_file(base)
