from random import randint

from PIL import Image, ImageDraw

from utils import http
from utils.endpoint import Endpoint, setup
from utils.textutils import wrap, render_text_with_emoji
from utils.perspective import circle_crop, convert_fit


@setup
class Youtube(Endpoint):
    def generate(self, kwargs):
        image_url = kwargs['avatar']
        username = kwargs['username']
        text = kwargs['text']

        avatar = convert_fit(http.get_image(image_url), (52, 52))
        base = Image.open(self.get_asset('youtube.bmp')).convert('RGBA')
        font = self.assets.get_font('robotomedium.ttf', size=17)
        font2 = self.assets.get_font('robotoregular.ttf', size=19)

        avatar = circle_crop(avatar)

        base.paste(avatar, (17, 33), avatar)
        canv = ImageDraw.Draw(base)
        op = wrap(font, username, 1150)
        size = canv.textsize(username, font=font)
        comment = wrap(font2, text, 550)
        num = randint(1, 40)
        plural = '' if num == 1 else 's'
        time = f'{num} minute{plural} ago'
        render_text_with_emoji(base, canv, (92, 34), op, font=font, fill='Black')
        render_text_with_emoji(base, canv, (100 + size[0], 34), time, font=font, fill='Grey')
        render_text_with_emoji(base, canv, (92, 59), comment, font=font2, fill='Black')
        base = base.convert('RGBA')

        return self.send_file(base)