from PIL import Image, ImageDraw

from utils.endpoint import Endpoint, setup
from utils.textutils import wrap, render_text_with_emoji


@setup
class Note(Endpoint):
    def generate(self, kwargs):
        text = kwargs['text']
        base = Image.open(self.get_asset('note.bmp')).convert('RGBA')
        # We need a text layer here for the rotation
        text_layer = Image.new('RGBA', base.size)
        font = self.assets.get_font('sans.ttf', size=16)
        canv = ImageDraw.Draw(text_layer)

        text = wrap(font, text, 150)
        render_text_with_emoji(text_layer, canv, (455, 420), text, font=font, fill='Black')

        text_layer = text_layer.rotate(-23, resample=Image.BICUBIC)

        base.paste(text_layer, (0, 0), text_layer)
        base = base.convert('RGB')

        return self.send_file(base, format='jpeg')