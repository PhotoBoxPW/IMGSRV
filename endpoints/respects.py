from PIL import Image

from utils import http
from utils.endpoint import Endpoint, setup
from utils.perspective import convert_fit, skew


@setup
class Respects(Endpoint):
    def generate(self, kwargs):
        image_url = kwargs['image']

        base = Image.open(self.get_asset('respects.bmp'))
        white = Image.new('RGBA', (base.width, base.height), 'black')
        img = convert_fit(http.get_image(image_url), (110, 110))

        img = skew(img, [(366, 91), (432, 91), (439, 191), (378, 196)])
        white.paste(img, (0, 0), img)
        white.paste(base, (0, 0), base)
        white = white.convert('RGB')

        return self.send_file(white, format='jpeg')