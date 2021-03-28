from PIL import Image

from utils import http
from utils.endpoint import Endpoint, setup
from utils.perspective import convert_fit


@setup
class Whodidthis(Endpoint):
    def generate(self, kwargs):
        image_url = kwargs['image']

        base = Image.open(self.get_asset('whodidthis.bmp'))
        avatar = convert_fit(http.get_image(image_url), (720, 405))
        base.paste(avatar, (0, 159), avatar)

        base = base.convert('RGBA')
        return self.send_file(base)
