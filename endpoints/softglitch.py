from random import randint

from utils import http
from utils.endpoint import Endpoint, setup
from utils.perspective import box_resize
from utils.glitch import soft_glitch


@setup
class SoftGlitch(Endpoint):
    def generate(self, kwargs):
        image_url = kwargs['image']

        img = http.get_image(image_url)
        img = box_resize(img, 500)
        img = img.convert('RGBA')
        img = soft_glitch(img, glitch_amount=randint(3, 5), color_offset=True, scan_lines=True)

        return self.send_file(img)