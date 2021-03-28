from random import randint

from utils import http
from utils.endpoint import Endpoint, setup
from utils.perspective import box_resize
from utils.glitch import add_noise_bands, low_res_blocks, shift_corruption, sin_wave_distortion, split_color_channels, walk_distortion


@setup
class Glitch(Endpoint):
    def generate(self, kwargs):
        image_url = kwargs['image']

        img = http.get_image(image_url)
        original_res = False if not 'original_res' in kwargs else bool(kwargs['original_res'])
        if not original_res: img = box_resize(img, 500)
        img = img.convert('RGBA')
        #img = pixel_sort(img, mask_function=lambda val: 255 if val < 100 else 0)
        img = split_color_channels(img, offset=1)
        img = add_noise_bands(img, count=4, thickness=10)
        img = sin_wave_distortion(img, mag=3, freq=1)
        img = walk_distortion(img, max_step_length=1)
        img = shift_corruption(img, offset_mag=2, coverage=0.25)
        img = low_res_blocks(img, rows=15, cols=15, cells=4, factor=2)

        return self.send_file(img)