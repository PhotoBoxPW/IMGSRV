from random import randint

from PIL import Image

from utils import http
from utils.endpoint import Endpoint, setup


@setup
class Triggered(Endpoint):
    def generate(self, kwargs):
        image_url = kwargs['image']

        avatar = http.get_image(image_url).resize((320, 320)).convert('RGBA')
        triggered = Image.open(self.get_asset('triggered.bmp'))
        tint = Image.open(self.get_asset('red.bmp')).convert('RGBA')
        blank = Image.new('RGBA', (256, 256), color=(231, 19, 29))
        frames = []

        for i in range(8):
            base = blank.copy()

            if i == 0:
                base.paste(avatar, (-16, -16), avatar)
            else:
                base.paste(avatar, (-32 + randint(-16, 16), -32 + randint(-16, 16)), avatar)

            base.paste(tint, (0, 0), tint)

            if i == 0:
                base.paste(triggered, (-10, 200))
            else:
                base.paste(triggered, (-12 + randint(-8, 8), 200 + randint(0, 12)))

            frames.append(base)

        return self.send_file(frames[0], save_all=True, append_images=frames[1:], format='gif', loop=0, duration=20, disposal=2,
                       optimize=True)
