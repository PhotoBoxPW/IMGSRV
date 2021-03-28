from PIL import Image, ImageOps

from utils.endpoint import SimpleFilter, setup


@setup
class Blurple(SimpleFilter):
    def use_filter(self, img, kwargs):
        img = img.convert('RGBA')
        toned = img.convert('L')
        toned = ImageOps.colorize(toned, (27, 31, 51), (255, 255, 255), (114, 137, 218))

        base = Image.new('RGBA', img.size)
        base.paste(toned, (0, 0), img)
        return base


