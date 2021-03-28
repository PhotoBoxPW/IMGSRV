from PIL import Image

from utils import http
from utils.endpoint import Endpoint, setup
from utils.transparent_gif import create_animated_gif
from utils.perspective import convert_fit


@setup
class Spin(Endpoint):
    def generate(self, kwargs):
        image_url = kwargs['image']

        img = convert_fit(http.get_image(image_url), (256, 256))

        out = []
        steps = 30
        for i in range(0, steps):
            frame = img.copy().convert('RGBA').rotate(i * (360/steps), resample=Image.BICUBIC)
            height_diff = frame.height - img.height
            width_diff = frame.width - img.width
            frame = frame.crop((
                int(width_diff / 2), int(height_diff / 2), frame.width - int(width_diff / 2),
                frame.height - int(height_diff / 2)))
            out.append(frame)

        root_frame, save_args = create_animated_gif(out, 50)
        return self.send_file(root_frame, **save_args, comment="Made by PhotoBox (photobox.pw)")