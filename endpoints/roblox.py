from PIL import Image

from utils import http
from utils.endpoint import Endpoint, setup
from utils.perspective import convert_fit, skew


@setup
class Roblox(Endpoint):
    def generate(self, kwargs):
        image_url = kwargs['image']

        base = Image.open(self.get_asset('roblox.bmp')).convert('RGBA')
        avatar = convert_fit(http.get_image(image_url), (256, 256))
        avatar = skew(avatar, [(138, 122), (263, 130), (252, 262), (147, 234)])
        base.paste(avatar, (0, 0), avatar)

        return self.send_file(base)