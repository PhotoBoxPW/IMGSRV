from PIL import Image, ImageColor, ImageOps

from utils.endpoint import SimpleFilter, setup


@setup
class Mtndew(SimpleFilter):
    def use_filter(self, img, kwargs):
        light = ImageColor.getrgb('#FBF019')
        dark = ImageColor.getrgb('#01AB6D')

        img = img.convert('RGBA')
        toned = img.convert('L')
        toned = ImageOps.colorize(toned, dark, light)

        base = Image.new('RGBA', img.size)
        base.paste(toned, (0, 0), img)
        return base