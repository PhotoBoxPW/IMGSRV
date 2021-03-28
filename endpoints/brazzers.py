from PIL import Image

from utils import http
from utils.endpoint import Endpoint, setup


@setup
class Brazzers(Endpoint):
    def generate(self, kwargs):
        image_url = kwargs['image']

        avatar = http.get_image(image_url).convert('RGBA')
        base = Image.open(self.get_asset('brazzers.bmp'))
        aspect = avatar.width / avatar.height

        new_height = int(base.height * aspect)
        new_width = int(base.width * aspect)
        scale = new_width / avatar.width
        size = (int(new_width / scale / 2), int(new_height / scale / 2))

        base = base.resize(size).convert('RGBA')

        # avatar is technically the base
        avatar.paste(base, (avatar.width - base.width,
                            avatar.height - base.height), base)
        avatar = avatar.convert('RGBA')

        return self.send_file(avatar)