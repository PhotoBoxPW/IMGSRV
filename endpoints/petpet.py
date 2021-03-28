from PIL import Image, ImageOps

from utils import http
from utils.endpoint import Endpoint, setup
from utils.transparent_gif import create_animated_gif
from utils.perspective import contain


@setup
class Petpet(Endpoint):
    def generate(self, kwargs):
        image_url = kwargs['image']

        img = http.get_image(image_url).convert('RGBA')
        img = ImageOps.pad(img, (98, 93), method=Image.LANCZOS)
        #if img.width >= img.height:
        #    aspect = img.height / img.width
        #    img = img.resize((98, int(aspect * 93)))
        #else:
        #    aspect = img.width / img.height
        #    img = img.resize((int(aspect * 98), 93))
        hand = Image.open(self.get_asset('petpet.gif'))

        # (x, y, width, height)
        offsets = [
            (0, 0, 0, 0),
            (-4, 12, 4, -12),
            (-12, 18, 12, -18),
            (-8, 12, 4, -12),
            (-4, 0, 0, 0)
        ]
        out = []
        for i in range(0, 5):
            x, y, w, h = offsets[i]
            frame = Image.new('RGBA', (hand.width, hand.height))
            hand.seek(i)
            hand_frame = hand.copy().convert('RGBA')
            img_frame = img.copy().convert('RGBA')
            if w != 0 or h != 0:
                img_frame = img_frame.resize((img_frame.width + w, img_frame.height + h))
            frame.paste(img_frame, (14 + x, 20 + y), img_frame)
            frame.paste(hand_frame, (0, 0), hand_frame)
            out.append(frame)

        root_frame, save_args = create_animated_gif(out, 50)
        return self.send_file(root_frame, **save_args)
        #b = BytesIO()
        #root_frame, save_args = create_animated_gif(out, 50)
        #root_frame.save(b, **save_args)
        #b.seek(0)
        #return send_file(b, mimetype='image/gif')