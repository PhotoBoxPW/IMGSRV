from PIL import Image, ImageColor, ImageOps

from utils.endpoint import SimpleFilter, setup


@setup
class FireEngine(SimpleFilter):
    def use_filter(self, img, kwargs):
        light = ImageColor.getrgb('#F00E2E')
        dark = ImageColor.getrgb('#0A0505')

        img = img.convert('RGBA')
        toned = img.convert('L')
        toned = ImageOps.colorize(toned, dark, light)

        base = Image.new('RGBA', img.size)
        base.paste(toned, (0, 0), img)
        return base