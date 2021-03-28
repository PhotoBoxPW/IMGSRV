from PIL import Image, ImageColor, ImageOps

from utils.endpoint import SimpleFilter, setup


@setup
class Honeyglow(SimpleFilter):
    def use_filter(self, img, kwargs):
        light = ImageColor.getrgb('#FFCB00')
        dark = ImageColor.getrgb('#38046C')

        img = img.convert('RGBA')
        toned = img.convert('L')
        toned = ImageOps.colorize(toned, dark, light)

        base = Image.new('RGBA', img.size)
        base.paste(toned, (0, 0), img)
        return base