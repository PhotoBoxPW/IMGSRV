from PIL import Image

from utils import http
from utils.endpoint import Endpoint, setup
from utils.perspective import convert_fit, skew

@setup
class Linus(Endpoint):
    def generate(self, kwargs):
        image_url = kwargs['image']

        base = Image.open(self.get_asset('linus.bmp'))
        white = Image.new('RGBA', (base.width, base.height), 'black')
        img = convert_fit(http.get_image(image_url), (800, 450))

        img = skew(img, [(58, 184), (369, 143), (392, 402), (108, 563)])
        white.paste(img, (0, 0), img)
        white.paste(base, (0, 0), base)
        white = white.convert('RGB')

        return self.send_file(white, format='jpeg')