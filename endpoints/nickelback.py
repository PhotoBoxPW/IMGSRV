from PIL import Image

from utils import http
from utils.endpoint import Endpoint, setup
from utils.perspective import convert_fit, skew

@setup
class Nickelback(Endpoint):
    def generate(self, kwargs):
        image_url = kwargs['image']

        base = Image.open(self.get_asset('nickelback.bmp'))
        white = Image.new('RGBA', (base.width, base.height), '#ddd')
        img = convert_fit(http.get_image(image_url), (800, 450))

        img = skew(img, [(489, 287), (859, 192), (909, 446), (550, 537)])
        white.paste(img, (0, 0), img)
        white.paste(base, (0, 0), base)
        white = white.convert('RGB')

        return self.send_file(white, format='jpeg')