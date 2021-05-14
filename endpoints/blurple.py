from PIL import Image, ImageOps

from utils.endpoint import SimpleFilter, setup


@setup
class Blurple(SimpleFilter):
    def use_filter(self, img, kwargs):
        new_color = False if not 'new_color' in kwargs else bool(kwargs['new_color'])

        img = img.convert('RGBA')
        toned = img.convert('L')

        if new_color:
            toned = ImageOps.colorize(toned, (25, 30, 73), (255, 255, 255), (88, 101, 241))
        else:
            toned = ImageOps.colorize(toned, (27, 31, 51), (255, 255, 255), (114, 137, 218))

        base = Image.new('RGBA', img.size)
        base.paste(toned, (0, 0), img)
        return base


