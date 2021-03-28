from PIL import Image, ImageDraw, ImageOps

from utils.endpoint import Endpoint, setup
from utils.textutils import render_text_with_emoji, wrap, auto_text_size
from utils.perspective import skew, center_content

@setup
class AnimeProtest(Endpoint):
    def generate(self, kwargs):
        text = kwargs['text']

        # generate text layer
        text_base = Image.new('RGBA', (300, 200))
        #font, text = auto_text_size(text, self.assets.get_font('sunshine.ttf'), 250, fallback_size=50, font_scalar=4, range=range(10, 60))
        font = self.assets.get_font('sunshine.ttf', size=60)
        canv = ImageDraw.Draw(text_base)
        render_text_with_emoji(text_base, canv, (0, 0), wrap(font, text, 200), font, 'black')
        #render_text_with_emoji(text_base, canv, (0, 0), text, font, 'black')
        text_base = center_content(text_base)
        text_base = skew(text_base, [(67, 6), (175, 9), (168, 95), (62, 90)])

        base = Image.open(self.get_asset('animeprotest.bmp'))
        white = Image.new('RGBA', (base.width, base.height), '#f9f7f8')

        white.paste(text_base, (0, 0), text_base)
        white.paste(base, (0, 0), base)
        white = white.convert('RGB')

        return self.send_file(white, format='jpeg')