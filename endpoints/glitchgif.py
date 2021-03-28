from math import cos, pi
from PIL import Image, ImageOps
from apng import APNG

from utils import http
from utils.endpoint import Endpoint, setup
from utils.perspective import box_resize
from utils.glitch import add_noise_bands, low_res_blocks, pixel_sort, sin_wave_distortion, split_color_channels
from utils.transparent_gif import create_animated_gif


@setup
class GlitchGIF(Endpoint):
    def generate(self, kwargs):
        image_url = kwargs['image']
        allow_gifs = False if not 'allow_gif' in kwargs else bool(kwargs['allow_gif'])

        img, raw = http.get_image_and_raw(image_url)
        img = box_resize(img, 500)

        is_gif = hasattr(img, 'n_frames') and img.n_frames != 1 and allow_gifs

        if is_gif:
            frames = img.n_frames
            duration = img.info['duration']
            if img.format == 'PNG':
                apng = APNG.from_bytes(raw)
                duration_list = list(map(lambda tupl: float(tupl[1].delay) / float(tupl[1].delay_den) * 1000, apng.frames))
                if len(duration_list) != 0: duration = duration_list
        else:
            frames = 20
            duration = 60
            img = img.convert('RGBA')

        median_lum = 128
        lum_limit = median_lum + 0.5 * median_lum  # <- pixel sorting strength
        lum_limit = abs(lum_limit) if lum_limit <= 255 else 255
        out = []
        for i in range(0, frames):
            progress = ((i+1)/frames)
            loop_progress = -cos(2 * pi * progress)/2 + 0.5
            mask_func = lambda val, factor=loop_progress, limit=lum_limit:\
                255 if val < limit * factor else 0

            if is_gif:
                img.seek(i)
                frame = img.copy().convert('RGBA')
            else:
                frame = img.copy()
            frame = pixel_sort(frame, reverse=True, mask_function=mask_func)
            frame = sin_wave_distortion(frame, mag=5, freq=1, phase=-2*pi*progress)
            frame = add_noise_bands(frame, count=int(10 * loop_progress), thickness=10)
            frame = low_res_blocks(frame, rows=10, cols=10, cells=int(10 * progress), factor=4)
            # frame = ImageOps.posterize(frame, bits=int(5 * (1 - loop_progress) + 3))
            frame = split_color_channels(frame, offset=int(5 * loop_progress))
            # frame = frame.convert('P', palette=Image.ADAPTIVE)
            out.append(frame)

        root_frame, save_args = create_animated_gif(out, duration)
        return self.send_file(root_frame, **save_args, comment="Made by PhotoBox (photobox.pw)")