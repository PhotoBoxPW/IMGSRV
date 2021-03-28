from PIL import Image

from utils import http
from utils.endpoint import Endpoint, setup
from utils.perspective import convert_fit, skew
from utils.color_ops import get_color


@setup
class StarVSTheForcesOf(Endpoint):
    def generate(self, kwargs):
        image_url = kwargs['image']

        base = Image.open(self.get_asset('starvstheforcesof.bmp'))
        white = Image.new('RGBA', (base.width, base.height), 'black')
        img = convert_fit(http.get_image(image_url), (700, 700))

        # set up tint
        base_mask = Image.open(self.get_asset('mask.bmp'))
        color = get_color(img)
        tint = Image.new('RGBA', (base.width, base.height), color)

        distance = 948
        next_dist = 1920 - distance
        img = skew(img, [(0, 150), (next_dist, 0), (next_dist, 1280), (0, 1180)], resolution=1280)

        white.paste(img, (distance, -120), img)
        white.paste(base, (0, 0), base)
        white.paste(tint, (0, 0), base_mask)
        white = white.convert('RGB')

        return self.send_file(white, format='jpeg')