from PIL import Image, ImageEnhance, ImageOps

from utils import http
from utils.endpoint import SimpleFilter, setup


@setup
class DeepFry(SimpleFilter):
    fmt = 'jpeg'

    # Using code from https://github.com/Ovyerus/deeppyer
    # because the original code was not that good tbh
    def use_filter(self, img, kwargs):
        img = img.convert('RGB')

        # Crush image to hell and back
        width, height = img.width, img.height
        img = img.resize((int(width ** .75), int(height ** .75)), resample=Image.LANCZOS)
        img = img.resize((int(width ** .88), int(height ** .88)), resample=Image.BILINEAR)
        img = img.resize((int(width ** .9), int(height ** .9)), resample=Image.BICUBIC)
        img = img.resize((width, height), resample=Image.BICUBIC)
        img = ImageOps.posterize(img, 4)

        # Generate colour overlay
        r = img.split()[0]
        r = ImageEnhance.Contrast(r).enhance(2.0)
        r = ImageEnhance.Brightness(r).enhance(1.5)

        r = ImageOps.colorize(r, (254, 0, 2), (255, 255, 15))

        # Overlay red and yellow onto main image and sharpen the hell out of it
        img = Image.blend(img, r, 0.75)
        img = ImageEnhance.Sharpness(img).enhance(100.0)

        return img