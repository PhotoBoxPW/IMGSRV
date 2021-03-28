from PIL import Image

from utils import http
from utils.endpoint import Endpoint, setup

@setup
class Ship(Endpoint):
    def generate(self, kwargs):
        base = Image.new('RGBA', (450, 150))
        heart_type = 'red' if not 'heart' in kwargs else kwargs['heart']
        heart = Image.open(self.get_asset(f'{heart_type}.bmp'))
        img1 = http.get_image(kwargs['avatar1']).resize((150, 150)).convert('RGBA')
        img2 = http.get_image(kwargs['avatar2']).resize((150, 150)).convert('RGBA')

        base.paste(heart, (165, 15))
        base.paste(img1, (0, 0), img1)
        base.paste(img2, (base.width - 150, 0), img2)

        return self.send_file(base)