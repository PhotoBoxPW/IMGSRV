from PIL import Image, ImageOps

from utils import http
from utils.endpoint import Endpoint, setup
from utils.perspective import skew

@setup
class Clint(Endpoint):
    def generate(self, kwargs):
        image_url = kwargs['image']

        base = Image.open(self.get_asset('clint.bmp'))
        white = Image.new('RGBA', (base.width, base.height), 'black')
        img = http.get_image(image_url).convert('RGBA')
        img = ImageOps.fit(img, (700, 700), method=Image.LANCZOS)

        distance = 782
        next_dist = 1112 - distance
        img = skew(img, [(0, 132), (next_dist, 0), (next_dist, 700), (0, 530)])

        white.paste(img, (distance, 0), img)
        white.paste(base, (0, 0), base)
        white = white.convert('RGB')

        return self.send_file(white, format='jpeg')