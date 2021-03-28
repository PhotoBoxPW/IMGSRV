from apng import APNG

from utils import http
from utils.endpoint import Endpoint, setup
from utils.transparent_gif import create_animated_gif
from utils.color_ops import shift_hsv
from utils.perspective import box_resize


@setup
class HueSpinGif(Endpoint):
    def generate(self, kwargs):
        image_url = kwargs['image']
        allow_gifs = False if not 'allow_gif' in kwargs else bool(kwargs['allow_gif'])

        img, raw = http.get_image_and_raw(image_url)
        img = box_resize(img, 500)

        is_gif = hasattr(img, 'n_frames') and img.n_frames != 1 and allow_gifs

        if is_gif:
            steps = img.n_frames
            duration = img.info['duration']
            if img.format == 'PNG':
                apng = APNG.from_bytes(raw)
                duration_list = list(map(lambda tupl: float(tupl[1].delay) / float(tupl[1].delay_den) * 1000, apng.frames))
                if len(duration_list) != 0: duration = duration_list
        else:
            steps = 35
            duration = 60
            img = img.convert('RGBA')

        out = []
        hue_per_step = 360.0 / steps
        for i in range(0, steps):
            if is_gif:
                img.seek(i)
                frame = img.copy().convert('RGBA')
            else:
                frame = img.copy()
            if i != 0:
                frame = shift_hsv(frame, hue=hue_per_step * i)
            out.append(frame)

        root_frame, save_args = create_animated_gif(out, duration)
        return self.send_file(root_frame, **save_args, comment="Made by PhotoBox (photobox.pw)")