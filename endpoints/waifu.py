from PIL import Image

from utils import http
from utils.endpoint import Endpoint, setup
from utils.perspective import convert_fit, skew

@setup
class Waifu(Endpoint):
    def generate(self, kwargs):
        image_url = kwargs['image']

        base = Image.open(self.get_asset('waifu.bmp'))
        white = Image.new('RGBA', (base.width, base.height), 'white')
        img = convert_fit(http.get_image(image_url), (220, 400), mode='LA')
        img = img.convert('RGBA')

        img = skew(img, [(151, 178), (252, 202), (199, 351), (97, 321)])
        white.paste(img, (0, 0), img)
        white.paste(base, (0, 0), base)
        white = white.convert('RGB')

        return self.send_file(white, format='jpeg')