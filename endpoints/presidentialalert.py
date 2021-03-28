from PIL import Image, ImageDraw

from utils.endpoint import Endpoint, setup
from utils.textutils import render_text_with_emoji, wrap


@setup
class PresidentialAlert(Endpoint):
    def generate(self, kwargs):
        text = kwargs['text']

        base = Image.open(self.get_asset('presidentialalert.bmp'))
        font = self.assets.get_font('sfprodisplay.ttf', size=38)
        canv = ImageDraw.Draw(base)
        render_text_with_emoji(base, canv, (60, 830), wrap(font, text, 1120), font=font, fill='black')

        return self.send_file(base)
