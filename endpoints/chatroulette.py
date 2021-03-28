from PIL import Image, ImageOps

from utils import http
from utils.endpoint import Endpoint, setup
from utils.perspective import skew

@setup
class Chatroulette(Endpoint):
    def generate(self, kwargs):
        image_url = kwargs['image']

        base = Image.open(self.get_asset('chatroulette.bmp'))
        img = http.get_image(image_url).convert('RGBA')
        img = ImageOps.pad(img, (320, 240), method=Image.LANCZOS)
        base.paste(img, (18, 349), img)
        base = base.convert('RGB')

        return self.send_file(base, format='jpeg')