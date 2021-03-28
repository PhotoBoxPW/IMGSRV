from PIL import Image, ImageDraw

from utils.endpoint import Endpoint, setup
from utils.textutils import render_text_with_emoji, wrap


@setup
class BonziBuddy(Endpoint):
    def generate(self, kwargs):
        text = kwargs['text']

        base = Image.open(self.get_asset('bonzibuddy.bmp'))
        font = self.assets.get_font('arial.ttf', size=20)
        canv = ImageDraw.Draw(base)
        render_text_with_emoji(base, canv, (19, 12), wrap(font, text, 187), font, 'black')

        return self.send_file(base)
