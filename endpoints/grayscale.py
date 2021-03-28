from utils.endpoint import SimpleFilter, setup


@setup
class Grayscale(SimpleFilter):
    def use_filter(self, img, kwargs):
        img = img.convert('LA')
        return img
