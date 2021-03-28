from PIL import Image

from utils import http
from utils.endpoint import Endpoint, setup
from utils.perspective import convert_fit

@setup
class Art(Endpoint):
    def generate(self, kwargs):
        image_url = kwargs['image']

        base = Image.open(self.get_asset('art.bmp'))
        white = Image.new('RGBA', (base.width, base.height), '#fbe7fc')
        img1 = convert_fit(http.get_image(image_url), (370, 370))

        white.paste(img1, (903, 92), img1)
        white.paste(img1, (903, 860), img1)
        white.paste(base, (0, 0), base)
        white = white.convert('RGB')

        return self.send_file(white, format='jpeg')