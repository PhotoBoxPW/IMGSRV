from PIL import Image

from utils import http
from utils.endpoint import Endpoint, setup
from utils.perspective import convert_fit


@setup
class Shoot(Endpoint):
    def generate(self, kwargs):
        image_url = kwargs['image']

        base = Image.open(self.get_asset('shoot.bmp'))
        avatar = convert_fit(http.get_image(image_url), base.size)
        avatar.paste(base, (0, 0), base)

        return self.send_file(avatar)