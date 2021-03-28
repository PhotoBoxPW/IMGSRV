from PIL import Image, ImageOps

from utils import http
from utils.endpoint import Endpoint, setup

@setup
class Studying(Endpoint):
    def generate(self, kwargs):
        image_url = kwargs['image']

        base = Image.open(self.get_asset('studying.bmp'))
        white = Image.new('RGBA', (base.width, base.height), 'black')
        img = http.get_image(image_url).convert('RGBA')
        img = ImageOps.fit(img, (276, 248), method=Image.LANCZOS)
        img = ImageOps.mirror(img)

        white.paste(img, (92, 198), img)
        white.paste(base, (0, 0), base)
        white = white.convert('RGB')

        return self.send_file(white, format='jpeg')