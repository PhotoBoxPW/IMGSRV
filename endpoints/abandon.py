from PIL import Image, ImageDraw

from utils.endpoint import Endpoint, setup
from utils.textutils import render_text_with_emoji, wrap


@setup
class Abandon(Endpoint):
    def generate(self, kwargs):
        text = kwargs['text']

        base = Image.open(self.get_asset('abandon.bmp'))
        font = self.assets.get_font('verdana.ttf', size=24)
        canv = ImageDraw.Draw(base)
        render_text_with_emoji(base, canv, (25, 413), wrap(font, text, 320), font, 'black')

        base = base.convert('RGB')
        return self.send_file(base, format='jpeg')
