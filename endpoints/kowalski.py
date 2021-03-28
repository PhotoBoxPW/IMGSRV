from PIL import Image, ImageDraw

from utils.endpoint import Endpoint, setup
from utils.textutils import render_text_with_emoji, wrap
from utils.perspective import skew


@setup
class Kowalski(Endpoint):
    def generate(self, kwargs):
        text = kwargs['text']

        # generate text layer
        text_base = Image.new('RGBA', (400, 300))
        font = self.assets.get_font('verdana.ttf', size=40)
        canv = ImageDraw.Draw(text_base)
        render_text_with_emoji(text_base, canv, (0, 0), wrap(font, text, 400), font, 'black')
        text_base = skew(text_base, [(350, 118), (568, 66), (597, 214), (356, 246)])

        # render gif frames with the text layer
        gif = Image.open(self.get_asset('kowalski.gif'))
        out = []
        for i in range(0, gif.n_frames):
            gif.seek(i)
            f = gif.copy().convert('RGBA')
            f.paste(text_base, (0, 0), text_base)
            out.append(f)

        return self.send_file(out[0], format='gif', save_all=True, append_images=out[1:], loop=0, disposal=2, optimize=True, duration=gif.info['duration'], comment="Made by PhotoBox (photobox.pw)")
