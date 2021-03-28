from PIL import Image, ImageDraw

from utils.endpoint import Endpoint, setup
from utils.textutils import render_text_with_emoji, wrap


@setup
class DogBite(Endpoint):
    def generate(self, kwargs):
        text = kwargs['text']

        base = Image.open(self.get_asset('dogbite.bmp'))
        font = self.assets.get_font('comic.ttf', size=21)
        canv = ImageDraw.Draw(base)
        render_text_with_emoji(base, canv, (19, 256), wrap(font, text, 218), font, 'black')

        base = base.convert('RGB')
        return self.send_file(base, format='jpeg')
