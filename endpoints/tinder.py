from PIL import Image

from utils import http
from utils.endpoint import Endpoint, setup

@setup
class Tinder(Endpoint):
    def generate(self, kwargs):
        base = Image.open(self.get_asset('tinder.bmp'))
        blank = Image.new('RGBA', (base.width, base.height))
        img1 = http.get_image(kwargs['avatar1']).resize((218, 218)).convert('RGBA')
        img2 = http.get_image(kwargs['avatar2']).resize((218, 218)).convert('RGBA')

        blank.paste(img1, (53, 288), img1)
        blank.paste(img2, (309, 288), img2)
        blank.paste(base, (0, 0), base)

        return self.send_file(blank)