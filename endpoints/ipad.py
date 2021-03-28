from PIL import Image

from utils import http
from utils.endpoint import Endpoint, setup
from utils.perspective import skew

@setup
class IPad(Endpoint):
    def generate(self, kwargs):
        image_url = kwargs['image']

        white = Image.new('RGBA', (2048, 1364), 0x00000000)
        base = Image.open(self.get_asset('ipad.bmp'))
        img1 = http.get_image(image_url).resize((512, 512), Image.LANCZOS).convert('RGBA')

        img1 = skew(img1, [(476, 484), (781, 379), (956, 807), (668, 943)])
        white.paste(img1, (0, 0), img1)
        white.paste(base, (0, 0), base)
        white = white.convert('RGB')

        return self.send_file(white, format='jpeg')