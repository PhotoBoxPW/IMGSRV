from PIL import ImageOps

from utils.endpoint import SimpleFilter, setup


@setup
class Flop(SimpleFilter):
    def use_filter(self, img, kwargs):
        img = img.convert('RGBA')
        img = ImageOps.flip(img)
        return img