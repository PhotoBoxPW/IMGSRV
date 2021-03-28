from PIL import Image, ImageOps

from utils import http
from utils.endpoint import Endpoint, setup
from utils.perspective import skew

@setup
class ScreamingBaby(Endpoint):
    def generate(self, kwargs):
        image_url = kwargs['image']

        base = Image.open(self.get_asset('screamingbaby.bmp'))
        white = Image.new('RGBA', (base.width, base.height), 'white')
        img = http.get_image(image_url).convert('RGBA')
        img = ImageOps.fit(img, (800, 600), method=Image.LANCZOS)

        img = skew(img, [(407, 867), (935, 618), (1116, 937), (630, 1275)])
        white.paste(img, (0, 0), img)
        white.paste(base, (0, 0), base)
        white = white.convert('RGB')

        return self.send_file(white, format='jpeg')