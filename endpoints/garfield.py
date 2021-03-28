from PIL import Image, ImageDraw

from utils.http import get_image
from utils.endpoint import Endpoint, setup


@setup
class Garfield(Endpoint):
    def generate(self, kwargs):
        image_url = kwargs['image']

        base = Image.open(self.get_asset('garfield.bmp')).convert('RGB')
        no_entry = Image.open(self.get_asset('no_entry.bmp')).convert('RGBA').resize((224, 224), Image.LANCZOS)
        avatar = get_image(image_url).resize((192, 192), Image.LANCZOS).convert('RGBA')

        base.paste(avatar, (282, 62), avatar)
        base.paste(no_entry, (266, 46), no_entry)

        return self.send_file(base, format='jpeg')