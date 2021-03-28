from PIL import Image

from utils.endpoint import SimpleFilter, setup


@setup
class Jpeg(SimpleFilter):
    fmt = 'jpeg'

    def use_filter(self, img, kwargs):
        quality = 3 if not 'quality' in kwargs else int(kwargs['quality'])
        quality = max(1, min(quality, 10))

        img = img.convert('RGB')

        # width, height = img.width, img.height
        # img = img.resize((int(width ** .75), int(height ** .75)), resample=Image.LANCZOS)
        # img = img.resize((int(width ** .88), int(height ** .88)), resample=Image.BILINEAR)
        # img = img.resize((int(width ** .9), int(height ** .9)), resample=Image.BICUBIC)
        # img = img.resize((width, height), resample=Image.BICUBIC)
        # img = ImageOps.posterize(img, 4)
        # img = ImageEnhance.Contrast(img).enhance(1)
        # img = ImageEnhance.Sharpness(img).enhance(100.0)

        bio = self.to_bytes(img, format='jpeg', quality=quality)
        n_img = Image.open(bio)

        return n_img