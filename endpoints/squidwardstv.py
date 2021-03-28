from PIL import Image

from utils import http
from utils.endpoint import Endpoint, setup
from utils.perspective import convert_fit, skew

@setup
class SquidwardsTV(Endpoint):
    def generate(self, kwargs):
        image_url = kwargs['image']

        base = Image.open(self.get_asset('squidwardstv.bmp'))
        white = Image.new('RGBA', (base.width, base.height), 'white')
        img = convert_fit(http.get_image(image_url), (800, 600))

        img = skew(img, [(530, 107), (983, 278), (783, 611), (362, 434)])
        white.paste(img, (0, 0), img)
        white.paste(base, (0, 0), base)
        white = white.convert('RGB')

        return self.send_file(white, format='jpeg')