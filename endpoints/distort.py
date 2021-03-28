from io import BytesIO
from random import choice, randint
from PIL import Image, ImageOps

from flask import send_file

from utils import gm, http
from utils.endpoint import Endpoint, setup
from utils.color_ops import shift_hsv
from utils.perspective import autocrop


@setup
class Distort(Endpoint):
    def generate(self, kwargs):
        image_url = kwargs['image']
        original_res = False if not 'original_res' in kwargs else bool(kwargs['original_res'])
        if not original_res: image = http.get_image(image_url).convert('RGBA')
        image = ImageOps.pad(image, (500, 500), method=Image.LANCZOS)
        image = autocrop(image)

        # shift!
        image = shift_hsv(image, hue=randint(10, 350)/360.0, saturation=(randint(60, 180)/100)/360.0)

        # implode! roll! swirl!
        implode = '-{}'.format(str(randint(3, 15)))
        roll = '+{}+{}'.format(randint(0, 256), randint(0, 256))
        swirl = '{}{}'.format(choice(["+", "-"]), randint(120, 180))
        concat = ['-implode', implode, '-roll', roll, '-swirl', swirl]
        output = gm.convert_raw(self.to_bytes(image).getvalue(), concat, 'png')

        # send!
        b = BytesIO(output)
        b.seek(0)
        return send_file(b, mimetype='image/png')
