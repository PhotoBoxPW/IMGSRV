from PIL import Image, ImageOps

from utils import http
from utils.endpoint import Endpoint, setup
from utils.perspective import skew

@setup
class Bolsonaro(Endpoint):
    def generate(self, kwargs):
        image_url = kwargs['image']

        base = Image.open(self.get_asset('bolsonaro.bmp'))
        white = Image.new('RGBA', (base.width, base.height), '#ddd')
        img = http.get_image(image_url).convert('RGBA')
        img = ImageOps.fit(img, (400, 220), method=Image.LANCZOS)

        img = skew(img, [(317, 66), (676, 61), (670, 262), (317, 259)])
        white.paste(img, (0, 0), img)
        white.paste(base, (0, 0), base)
        white = white.convert('RGB')

        return self.send_file(white, format='jpeg')