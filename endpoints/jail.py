from random import randint

from PIL import Image

from utils import http
from utils.endpoint import Endpoint, setup
from utils.perspective import convert_pad


@setup
class Jail(Endpoint):
    def generate(self, kwargs):
        image_url = kwargs['image']

        overlay = Image.open(self.get_asset('jail.bmp')).convert('RGBA')
        avatar = convert_pad(http.get_image(image_url), overlay.size)
        gray = avatar.convert('L')

        base = Image.new('RGBA', avatar.size)
        base.paste(gray, (0, 0), avatar)
        base.paste(overlay, (0, 0), overlay)

        return self.send_file(base)