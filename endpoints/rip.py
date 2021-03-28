from PIL import Image
import numpy as np

from utils import http
from utils.endpoint import Endpoint, setup
from utils.perspective import convert_fit


@setup
class Rip(Endpoint):
    def generate(self, kwargs):
        image_url = kwargs['image']

        # why are we resizing this?
        # @TODO don't resize rip asset on generation
        base = Image.open(self.get_asset('rip.bmp')).convert('RGBA').resize((642, 806))
        img = convert_fit(http.get_image(image_url), (300, 300), mode='LA')

        # translate L into A
        arr = np.array(img)
        overall_opacity = 0.8
        arr[..., 1] = 255 - arr[..., 0]
        arr[..., 1] = arr[..., 1] * overall_opacity
        arr[..., 0] = 0
        img = Image.fromarray(arr)

        img = img.convert('RGBA')
        base.paste(img, (175, 385), img)
        base = base.convert('RGBA')

        return self.send_file(base)