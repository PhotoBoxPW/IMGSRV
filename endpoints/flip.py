from PIL import ImageOps

from utils.endpoint import SimpleFilter, setup


@setup
class Flip(SimpleFilter):
    def use_filter(self, img, kwargs):
        img = img.convert('RGBA')
        img = ImageOps.mirror(img)
        return img