from PIL import Image, ImageOps

from utils.endpoint import SimpleFilter, setup


@setup
class Invert(SimpleFilter):
    def use_filter(self, img, kwargs):
        if img.mode == 'RGBA':
            r, g, b, a = img.split()
            rgb_image = Image.merge('RGB', (r, g, b))
            inverted = ImageOps.invert(rgb_image)
            r, g, b = inverted.split()
            img = Image.merge('RGBA', (r, g, b, a))
        else:
            img = img.convert('RGB')
            img = ImageOps.invert(img)

        img = img.convert('RGBA')
        return img
