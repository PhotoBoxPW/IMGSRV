from utils.endpoint import SimpleFilter, setup
from utils.perspective import circle_crop, convert_fit


@setup
class CircleCrop(SimpleFilter):
    def use_filter(self, img, kwargs):
        size = min(img.width, img.height)
        img = convert_fit(img, (size, size))
        img = circle_crop(img)
        return img