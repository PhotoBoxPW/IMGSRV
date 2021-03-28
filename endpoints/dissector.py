from PIL import Image, ImageOps

from utils import http
from utils.endpoint import Endpoint, setup
from utils.perspective import skew

@setup
class Dissector(Endpoint):
    def generate(self, kwargs):
        image_url = kwargs['image']

        base = Image.open(self.get_asset('dissector.bmp'))
        img = http.get_image(image_url).convert('RGBA')
        img = ImageOps.pad(img, (1000, 1000), method=Image.LANCZOS)
        img = skew(img, [(297, 208), (1120, 105), (1120, 960), (297, 1065)])

        base.paste(img, (0, 0), img)
        overlay = Image.open(self.get_asset('overlay.bmp'))
        base.paste(overlay, (0, 0), overlay)

        return self.send_file(base)