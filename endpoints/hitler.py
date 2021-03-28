from PIL import Image, ImageOps

from utils import http
from utils.endpoint import Endpoint, setup


@setup
class Hitler(Endpoint):
    def generate(self, kwargs):
        image_url = kwargs['image']

        base = Image.open(self.get_asset('hitler.bmp'))
        img1 = http.get_image(image_url).convert('RGBA')
        img1 = ImageOps.fit(img1, (140, 140), method=Image.LANCZOS)
        base.paste(img1, (46, 43), img1)
        base = base.convert('RGB')

        return self.send_file(base)