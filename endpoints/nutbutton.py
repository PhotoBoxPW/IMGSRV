from PIL import Image, ImageDraw

from utils.endpoint import Endpoint, setup
from utils.textutils import render_text_with_emoji, auto_text_size
from utils.perspective import center_content, skew


@setup
class NutButton(Endpoint):
    def generate(self, kwargs):
        text = kwargs['text']

        base = Image.open(self.get_asset('nutbutton.bmp'))

        font, text = auto_text_size(text, self.assets.get_font('impact.ttf'), 270, font_scalar=3)
        text_layer = Image.new('RGBA', (300, 300))
        canv = ImageDraw.Draw(text_layer)
        render_text_with_emoji(text_layer, canv, (0, 0), text, font, 'white')
        text_layer = center_content(text_layer)
        text_layer = skew(text_layer, [(28, 199), (261, 214), (317, 382), (32, 398)])

        base.paste(text_layer, (0, 0), text_layer)
        base = base.convert('RGB')
        return self.send_file(base, format='jpeg')
