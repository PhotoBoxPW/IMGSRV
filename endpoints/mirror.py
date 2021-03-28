from PIL import ImageOps

from utils.endpoint import SimpleFilter, setup


@setup
class Mirror(SimpleFilter):
    def use_filter(self, img, kwargs):
        img = img.convert('RGBA')
        half = round(img.width / 2)
        use_last_half = False if not 'last_half' in kwargs else bool(kwargs['last_half'])
        if use_last_half:
            first_half = img.crop((half, 0, img.width, img.height))
            second_half = img.crop((img.width - half, 0, img.width, img.height))
            second_half = ImageOps.mirror(second_half)

            second_half = second_half.crop((0, 0, img.width, img.height))
            second_half.paste(first_half, (img.width - half, 0), first_half)
            return second_half

        first_half = img.crop((0, 0, half, img.height))
        second_half = img.crop((0, 0, img.width - half, img.height))
        second_half = ImageOps.mirror(second_half)

        first_half = first_half.crop((0, 0, img.width, img.height))
        first_half.paste(second_half, (half, 0), second_half)
        return first_half