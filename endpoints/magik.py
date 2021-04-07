from io import BytesIO

from flask import send_file
from wand import image

from utils import http
from utils.endpoint import Endpoint, setup
from utils.exceptions import BadRequest
from utils.perspective import box_resize


@setup
class Magik(Endpoint):
    def generate(self, kwargs):
        image_url = kwargs['image']
        avatar_img = http.get_image(image_url)
        avatar_img = box_resize(avatar_img, 500)
        avatar = self.to_bytes(avatar_img)

        try:
            img = image.Image(file=avatar)
        except Exception as e:
            raise BadRequest(f'The image could not be loaded: {e}')

        try:
            multiplier = int(kwargs['mult'])
        except KeyError:
            multiplier = 1
        else:
            multiplier = max(min(multiplier, 10), 1)

        img.liquid_rescale(width=int(img.width * 0.5),
                           height=int(img.height * 0.5),
                           delta_x=0.5 * multiplier,
                           rigidity=0)
        img.liquid_rescale(width=int(img.width * 1.5),
                           height=int(img.height * 1.5),
                           delta_x=2 * multiplier,
                           rigidity=0)

        b = BytesIO()
        img.save(file=b)
        b.seek(0)
        img.destroy()
        return send_file(b, mimetype='image/png')
