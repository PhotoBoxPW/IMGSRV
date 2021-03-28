from PIL import Image
import numpy as np

from utils.endpoint import SimpleFilter, setup


@setup
class Sepia(SimpleFilter):
    def use_filter(self, img, kwargs):
        img = img.convert('RGBA')

        arr = np.array(img).astype('float')
        narr = np.zeros_like(arr)
        r, g, b = arr[..., 0], arr[..., 1], arr[..., 2]
        narr[..., 0] = np.clip(r * 0.393 + g * 0.769 + b * 0.189, 0.0, 255.0)
        narr[..., 1] = np.clip(r * 0.349 + g * 0.686 + b * 0.168, 0.0, 255.0)
        narr[..., 2] = np.clip(r * 0.272 + g * 0.534 + b * 0.131, 0.0, 255.0)
        narr[..., 3] = arr[..., 3]
        narr = narr.astype('uint8')

        return Image.fromarray(narr)
