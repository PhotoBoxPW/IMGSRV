from PIL import Image

from utils import http
from utils.endpoint import Endpoint, setup


@setup
class Disability(Endpoint):
    def generate(self, kwargs):
        image_url = kwargs['image']

        avatar = http.get_image(image_url).resize((175, 175)).convert('RGBA')
        base = Image.open(self.get_asset('disability.bmp')).convert('RGBA')

        base.paste(avatar, (450, 325), avatar)
        base = base.convert('RGBA')

        return self.send_file(base)