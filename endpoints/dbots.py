from PIL import Image, ImageOps

from utils import http
from utils.endpoint import Endpoint, setup

@setup
class DBots(Endpoint):
    def generate(self, kwargs):
        image_url = kwargs['image']
        no_overlay = False if not 'no_overlay' in kwargs else bool(kwargs['no_overlay'])

        base = Image.open(self.get_asset('dbots.bmp'))
        img = http.get_image(image_url).convert('RGBA')
        img = ImageOps.fit(img, (base.width, base.height), method=Image.LANCZOS)
        if not no_overlay:
            img.paste(base, (0, 0), base)
            img = img.convert('RGB')
        return self.send_file(img)