from PIL import Image, ImageDraw

from utils.endpoint import Endpoint, setup
from utils.textutils import auto_text_size, render_text_with_emoji


@setup
class Armor(Endpoint):
    def generate(self, kwargs):
        text = kwargs['text']

        base = Image.open(self.get_asset('armor.bmp')).convert('RGBA')
        # We need a text layer here for the rotation
        font, text = auto_text_size(text, self.assets.get_font('sans.ttf'), 207,
                                    font_scalar=0.8)
        canv = ImageDraw.Draw(base)

        render_text_with_emoji(base, canv, (34, 371), text, font=font, fill='Black')
        base = base.convert('RGB')

        return self.send_file(base, format='jpeg')