from PIL import Image

from utils import http
from utils.endpoint import Endpoint, setup


@setup
class Turkish(Endpoint):
    def generate(self, kwargs):
        image_url = kwargs['image']

        img1 = http.get_image(image_url).resize((256, 256)).convert('RGBA')
        img2 = Image.open(self.get_asset('turkish.gif'))
        img1.putalpha(128)

        out = []
        for i in range(0, img2.n_frames):
            img2.seek(i)
            f = img2.copy().resize((256, 256)).convert('RGBA')
            f.paste(img1, (0, 0), img1)
            out.append(f)

        return self.send_file(out[0], format='gif', save_all=True, append_images=out[1:], loop=0, disposal=2, optimize=True, duration=60)