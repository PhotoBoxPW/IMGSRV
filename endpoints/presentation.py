from PIL import Image, ImageDraw

from utils.endpoint import Endpoint, setup
from utils.textutils import wrap, render_text_with_emoji


@setup
class Presentation(Endpoint):
    def generate(self, kwargs):
        text = kwargs['text']
        base = Image.open(self.get_asset('presentation.bmp'))
        font = self.assets.get_font('verdana.ttf', size=24)
        canv = ImageDraw.Draw(base)
        text = wrap(font, text, 330)
        render_text_with_emoji(base, canv, (150, 80), text, font=font, fill='Black')

        base = base.convert('RGB')
        return self.send_file(base, format='jpeg')