from PIL import Image

from utils import http
from utils.endpoint import Endpoint, setup
from utils.perspective import convert_fit


@setup
class PhotoBox(Endpoint):
    def generate(self, kwargs):
        image_url = kwargs['image']

        img = convert_fit(http.get_image(image_url), (298, 298))
        imgbg = Image.new('RGBA', (298, 298), '#b3b3b3')
        imgbg.paste(img, (0, 0), img)

        base = Image.open(self.get_asset('photobox.bmp'))
        white = Image.new('RGBA', (base.width, base.height))
        white.paste(img, (483, 159), img)
        white.paste(base, (0, 0), base)

        return self.send_file(white)