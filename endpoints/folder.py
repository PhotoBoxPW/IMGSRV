from PIL import Image, ImageOps

from utils import http
from utils.endpoint import Endpoint, setup
from utils.perspective import skew

@setup
class Folder(Endpoint):
    def generate(self, kwargs):
        image_url = kwargs['image']

        base = Image.open(self.get_asset('folder.bmp'))
        white = Image.new('RGBA', (base.width, base.height), '#ddd')
        img = http.get_image(image_url).convert('RGBA')
        img = ImageOps.fit(img, (500, 500), method=Image.LANCZOS)

        img = skew(img, [(175, 54), (522, 142), (522, 510), (175, 422)])
        white.paste(img, (0, 0), img)
        white.paste(base, (0, 0), base)
        white = white.convert('RGB')

        return self.send_file(white, format='jpeg')