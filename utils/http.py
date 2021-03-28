import json
from io import BytesIO

import requests
from cairosvg import svg2png
from PIL import Image, ImageOps

from lottie.exporters import exporters
from lottie.importers import importers

from utils import exceptions

config = json.load(open('config.json'))
MAX_FILE_SIZE = config.get('max_file_size', 5 * 1024 * 1024)  # in bytes

def get(url, **kwargs):
    if config.get('new_proxy', False):
        proxies = config.get('proxies', {})
        res = requests.get(url, proxies=proxies, **kwargs)
    else:
        if 'proxy_url' in config:
            res = requests.get(config['proxy_url'],
                               params={'url': url},
                               headers={'Authorization': config['proxy_auth']},
                               **kwargs)
        else:
            res = requests.get(url, **kwargs)

    return res


def get_content_raw(url, **kwargs):
    return get(url, stream=True, **kwargs).content


def get_image(url, formats=None, **kwargs):
    return get_image_and_raw(url, formats=formats, **kwargs)[0]


def get_image_and_raw(url, formats=None, **kwargs):
    r = get(url, stream=True, timeout=5, **kwargs)
    r.raw.decode_content = True
    raw = r.raw.read(MAX_FILE_SIZE + 1)
    if len(raw) > MAX_FILE_SIZE:
        raise exceptions.InvalidImage(f'The image `{url}` is too large to be processed! (5MB max)')

    try:
        # raw = get_content_raw(url, **kwargs)

        b = None

        # Parse Lottie
        if raw[:8] == b'{"v":"5.':
           importer = importers.get('lottie')
           exporter = exporters.get('webp')
           an = importer.process(BytesIO(raw))
           b = BytesIO()
           exporter.process(an, b)
           b.seek(0)

        # Parse SVG
        if raw[:4] == b'<svg':
            raw = svg2png(bytestring=raw, scale=10)

        if b == None: b = BytesIO(raw)
        img = Image.open(b, formats=formats)

        # Trying to transpose with GIF/APNG files ruins the plugin
        if not hasattr(img, 'n_frames') or img.n_frames == 1:
            img = ImageOps.exif_transpose(img)
        return img, raw
    except OSError:
        raise exceptions.InvalidImage(f'An invalid image was provided from `{url}`! Check the URL and try again.')
