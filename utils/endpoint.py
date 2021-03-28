from abc import ABC, abstractmethod
from time import perf_counter
from utils.perspective import center_content

from utils import fixedlist
from utils.db import get_redis
from .asset_cache import AssetCache

from PIL import Image, ImageDraw
from io import BytesIO
from flask import send_file
from apng import APNG
from utils import http
from utils.transparent_gif import create_animated_gif
from utils.textutils import render_text_with_emoji, wrap

asset_cache = AssetCache()
endpoints = {}

buckets = {}


class Endpoint(ABC):
    def __init__(self, cache):
        self.avg_generation_times = fixedlist.FixedList(name=self.name, maximum_item_count=20)
        self.assets = cache

    @property
    def name(self):
        return self.__class__.__name__.lower()

    @property
    def bucket(self):
        return buckets.get(self.name)

    def get_avg_gen_time(self):
        if self.avg_generation_times.len() == 0:
            return 0

        return round(self.avg_generation_times.sum(), 2)

    def get_asset(self, item):
        return self.assets.get('assets/' + self.name + '/' + item)

    def run(self, **kwargs):
        get_redis().incr(self.name + ':hits')
        start = perf_counter()
        res = self.generate(kwargs)
        t = round((perf_counter() - start) * 1000, 2)  # Time in ms, formatted to 2dp
        self.avg_generation_times.append(t)
        return res

    def create_text_ladder(self, texts, border_width = 5, width = 500, fontname = 'verdana.ttf'):
        final = Image.new('RGB', ((width * 2) + border_width, 0), 'white')
        for index in range(len(texts)):
            base = Image.open(self.get_asset(f"ladder{index}.bmp"))
            aspect = base.height / base.width
            height = int(aspect * width)
            base = base.resize((width, height))

            # expand image
            base = base.crop((-(width + border_width), 0, base.width, base.height + border_width))

            # add white space for text
            whitespace = Image.new('RGB', (width, height), 'white')
            base.paste(whitespace, (0, 0))
            base = base.convert('RGB')

            # add text
            text = texts[index]
            #font = self.assets.get_font(fontname, size=30)
            #canv = ImageDraw.Draw(base)
            #render_text_with_emoji(base, canv, (border_width * 4, 40), wrap(font, text, width - (border_width * 8)), font, 'black')
            text_base = Image.new('RGBA', (width, height))
            font = self.assets.get_font(fontname, size=30)
            canv = ImageDraw.Draw(text_base)
            render_text_with_emoji(text_base, canv, (1, 0), wrap(font, text, width - (border_width * 8)), font, 'black')
            text_base = center_content(text_base)
            base.paste(text_base, (0, 0), text_base)
            base = base.convert('RGB')

            # push to final image
            final = final.crop((0, 0, final.width, final.height + base.height))
            final.paste(base, (0, final.height - base.height))
        if final.height != 0:
            final = final.crop((0, 0, final.width, final.height - border_width))
        return final

    def send_file(self, img, format='png', seek=0, mimetype=None, **save_args):
        if not mimetype: mimetype = 'image/' + format.lower()
        b = BytesIO()
        img.save(b, format=format, **save_args)
        b.seek(seek)
        return send_file(b, mimetype=mimetype)

    def to_bytes(self, img, format='png', seek=0, **save_args):
        b = BytesIO()
        img.save(b, format=format, **save_args)
        b.seek(seek)
        return b

    @abstractmethod
    def generate(self, kwargs):
        raise NotImplementedError(
            f"generate has not been implemented on endpoint {self.name}"
        )

class SimpleFilter(Endpoint):
    fmt = 'png'

    def generate(self, kwargs):
        image_url = kwargs['image']
        allow_gifs = False if not 'allow_gif' in kwargs else bool(kwargs['allow_gif'])

        img, raw = http.get_image_and_raw(image_url)
        is_gif = hasattr(img, 'n_frames') and img.n_frames != 1 and allow_gifs

        if not is_gif:
            img = self.use_filter(img, kwargs)
            return self.send_file(img, format=self.fmt)

        duration = img.info['duration']

        # Get durations from APNG
        if img.format == 'PNG':
            apng = APNG.from_bytes(raw)
            duration_list = list(map(lambda tupl: float(tupl[1].delay) / float(tupl[1].delay_den) * 1000, apng.frames))
            if len(duration_list) != 0: duration = duration_list

        out = []
        for i in range(0, img.n_frames):
            img.seek(i)
            frame = img.copy()
            frame = self.use_filter(frame, kwargs)
            out.append(frame)

        root_frame, save_args = create_animated_gif(out, duration)
        return self.send_file(root_frame, **save_args, comment="Made by PhotoBox (photobox.pw)")

    def use_filter(self, img, kwargs):
        raise NotImplementedError(
            f"use_filter has not been implemented on endpoint {self.name}"
        )


def setup(klass=None):
    if klass:
        kls = klass(asset_cache)
        endpoints[kls.name] = kls
        return kls
    else:
        def wrapper(klass, *a, **ka):
            kls = klass(asset_cache)
            endpoints[kls.name] = kls
            return kls
        return wrapper
