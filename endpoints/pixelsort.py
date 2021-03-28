from utils.endpoint import SimpleFilter, setup
from utils.perspective import box_resize
from utils.glitch import pixel_sort


@setup
class PixelSort(SimpleFilter):
    def use_filter(self, img, kwargs):
        original_res = False if not 'original_res' in kwargs else bool(kwargs['original_res'])
        if not original_res: img = box_resize(img, 500)
        img = img.convert('RGBA')
        img = pixel_sort(img, mask_function=lambda val: 255 if val < 100 else 0)
        return img