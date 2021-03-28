from PIL import Image, ImageOps

from utils import http
from utils.endpoint import Endpoint, setup

@setup
class DBotsPreview(Endpoint):
    def generate(self, kwargs):
        image_url = kwargs['image']

        base = Image.open(self.get_asset('dbotspreview.bmp'))
        white = Image.new('RGBA', (base.width, base.height), 'black')
        img = http.get_image(image_url).convert('RGBA')
        img = ImageOps.fit(img, (600, 338), method=Image.LANCZOS)

        white.paste(img, (171, 55), img)
        white.paste(base, (0, 0), base)
        white = white.convert('RGB')

        return self.send_file(white, format='jpeg')