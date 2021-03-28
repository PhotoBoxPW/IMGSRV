from PIL import Image, ImageOps

from utils import http
from utils.endpoint import Endpoint, setup
from utils.perspective import autocrop, box_resize

@setup
class IFunny(Endpoint):
    def generate(self, kwargs):
        image_url = kwargs['image']

        img = http.get_image(image_url).convert('RGBA')
        original_res = False if not 'original_res' in kwargs else bool(kwargs['original_res'])
        if not original_res: img = box_resize(img, 1000)

        # lazy way to size a watermark
        watermark = Image.open(self.get_asset('ifunny.bmp'))
        watermark = ImageOps.pad(watermark, (img.width, img.height), method=Image.LANCZOS)
        if watermark.getpixel((0, 0)) == (0, 0, 0, 0):
            watermark = autocrop(watermark)

        # Paste watermark
        height = img.height
        img = img.crop((0, 0, img.width, height + watermark.height))
        img.paste(watermark, (0, height), watermark)

        return self.send_file(img)