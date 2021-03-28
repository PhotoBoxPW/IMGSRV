from typing import Tuple
import numpy
from PIL import Image, ImageChops, ImageDraw, ImageOps


def find_coeffs(source_coords, target_coords):
    matrix = []
    for s, t in zip(source_coords, target_coords):
        matrix.append([t[0], t[1], 1, 0, 0, 0, -s[0] * t[0], -s[0] * t[1]])
        matrix.append([0, 0, 0, t[0], t[1], 1, -s[1] * t[0], -s[1] * t[1]])
    a = numpy.matrix(matrix, dtype=numpy.float)
    b = numpy.array(source_coords).reshape(8)
    res = numpy.dot(numpy.linalg.inv(a.T * a) * a.T, b)
    return numpy.array(res).reshape(8)


def skew(img, target_cords: list, source_coords: list=None, resolution: int=1024):
    # [(top_left), (top_right), (bottom_right), (bottom_left)]
    if source_coords:
        coeffs = find_coeffs(source_coords, target_cords)
    else:
        coeffs = find_coeffs([(0, 0), (img.width, 0), (img.width, img.height), (0, img.height)], target_cords)
    return img.transform((resolution, resolution), Image.PERSPECTIVE, coeffs,
                          Image.BICUBIC)


def contain(img, size: list, keep_border = True, method = Image.LANCZOS):
    w, h = size
    if img.width >= img.height:
        aspect = img.height / img.width
        new_height = int(aspect * h)
        bound = int((h - new_height) / 2)
        img = img.resize((w, new_height), method)
        if keep_border: img = img.crop((0, -bound, w, h - bound))
    else:
        aspect = img.width / img.height
        new_width = int(aspect * w)
        bound = int((w - new_width) / 2)
        img = img.resize((new_width, h), method)
        if keep_border: img = img.crop((-bound, 0, w - bound, h))
    return img


def box_resize(img, size: int, method = Image.LANCZOS):
    if not img.width > size and not img.height > size: return img
    if img.width >= img.height:
        aspect = img.height / img.width
        new_height = int(aspect * size)
        img = img.resize((size, new_height), method)
    else:
        aspect = img.width / img.height
        new_width = int(aspect * size)
        img = img.resize((new_width, size), method)
    return img


def autocrop(img, bg_pixel = (0,0), scale = 2.0, offset = -100):
    bg = Image.new(img.mode, img.size, img.getpixel(bg_pixel))
    diff = ImageChops.difference(img, bg)
    diff = ImageChops.add(diff, diff, scale, offset)
    bbox = diff.getbbox()
    if bbox: return img.crop(bbox)
    return img


def center_content(img, bg_pixel = (0,0), scale = 2.0, offset = -100):
    '''
    Centers auto-cropped content into its original size.
    Doesn't support color-filling. Didn't wanna do it.
    '''
    w = img.width
    h = img.height

    # Autocropping
    bg = Image.new(img.mode, img.size, img.getpixel(bg_pixel))
    diff = ImageChops.difference(img, bg)
    diff = ImageChops.add(diff, diff, scale, offset)
    bbox = diff.getbbox()
    if bbox: img = img.crop(bbox)
    else: return img

    # Get diff and re-add whitespace
    w_diff = w - img.width
    h_diff = h - img.height
    x_bound = round(w_diff / 2)
    y_bound = round(h_diff / 2)
    img = img.crop((-x_bound, -y_bound, img.width + (w_diff - x_bound), img.height + (h_diff - y_bound)))

    return img

def get_alpha_mask(img):
    mask_arr = numpy.array(img.convert('LA'))
    mask = Image.fromarray(mask_arr[..., 1], 'L')
    return mask

def border_radius(img, radius=10):
    circle = Image.new('L', (radius * 2, radius * 2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, radius * 2, radius * 2), fill=255)
    alpha = Image.new('L', img.size, 255)
    w, h = img.size
    alpha.paste(circle.crop((0, 0, radius, radius)), (0, 0))
    alpha.paste(circle.crop((0, radius, radius, radius * 2)), (0, h - radius))
    alpha.paste(circle.crop((radius, 0, radius * 2, radius)), (w - radius, 0))
    alpha.paste(circle.crop((radius, radius, radius * 2, radius * 2)), (w - radius, h - radius))
    mask = get_alpha_mask(img)
    diff = ImageChops.darker(mask, alpha)
    img.putalpha(diff)
    return img

def circle_crop(img):
    circle = Image.new('L', img.size, 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, img.width, img.height), fill=255)
    mask = get_alpha_mask(img)
    diff = ImageChops.darker(mask, circle)
    img.putalpha(diff)
    return img


def convert_fit(img, size: Tuple[int, int], method = Image.LANCZOS, mode = 'RGBA'):
    """
    Fits an image into a box, THEN converts,
    because we value our time(tm)
    """
    # realistically only saving 80 ms
    img = ImageOps.fit(img, size, method=method)
    img = img.convert(mode)
    return img


def convert_pad(img, size: Tuple[int, int], method = Image.LANCZOS, mode = 'RGBA'):
    """
    Pads an image into a box, THEN converts
    """
    img = ImageOps.pad(img, size, method=method)
    img = img.convert(mode)
    return img