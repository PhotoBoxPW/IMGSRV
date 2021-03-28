from PIL import Image, ImageDraw

from utils.endpoint import Endpoint, setup
from utils.textutils import wrap, render_text_with_emoji
from utils.perspective import skew, center_content


@setup
class ChangeMyMind(Endpoint):
    def generate(self, kwargs):
        text = kwargs['text']

        base = Image.open(self.get_asset('changemymind.bmp')).convert('RGBA')

        font = self.assets.get_font('arimobold.ttf', size=30)
        text_layer = Image.new('RGBA', (310, 150))
        canv = ImageDraw.Draw(text_layer)
        render_text_with_emoji(text_layer, canv, (0, 0), wrap(font, text, 310), font, 'black')
        text_layer = center_content(text_layer)
        text_layer = skew(text_layer, [(304, 333), (619, 200), (638, 333), (365, 449)])

        base.paste(text_layer, (0, 0), text_layer)
        base = base.convert('RGB')

        return self.send_file(base, format='jpeg')