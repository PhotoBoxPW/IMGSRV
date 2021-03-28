from PIL import ImageFilter

from utils.endpoint import SimpleFilter, setup


@setup
class Blur(SimpleFilter):
    def use_filter(self, img, kwargs):
        radius = 3 if not 'radius' in kwargs else int(kwargs['radius'])
        radius = max(2, min(radius, 10))
        img = img.convert('RGBA')
        img = img.filter(ImageFilter.GaussianBlur(radius=radius))
        return img