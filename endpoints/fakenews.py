from PIL import Image, ImageOps

from utils import http
from utils.endpoint import Endpoint, setup


@setup
class Fakenews(Endpoint):
    def generate(self, kwargs):
        image_url = kwargs['image']

        base = Image.open(self.get_asset('fakenews.bmp')).convert('RGBA')
        avatar = http.get_image(image_url).convert('RGBA')
        avatar = ImageOps.fit(avatar, (436, 252), method=Image.LANCZOS)
        final_image = Image.new('RGBA', base.size)

        # Put the base over the avatar
        final_image.paste(avatar, (372, 57), avatar)
        final_image.paste(base, (0, 0), base)
        final_image = final_image.convert('RGBA')

        return self.send_file(final_image)