import subprocess

from utils.http import get_content_raw


def convert(image: str, args: list, output_format: str):
    img_bytes = get_content_raw(image)
    return convert_raw(img_bytes, args, output_format)


def convert_raw(img_bytes, args: list, output_format: str):
    args = ['gm', 'convert', '-'] + args + ['{}:-'.format(output_format)]

    proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    stdout, stderr = proc.communicate(img_bytes)
    return stdout


def radial_blur(image: str, degrees: int, output_format: str):
    img_bytes = get_content_raw(image)
    args = [
        'convert', '-',
        '-rotational-blur', str(degrees),
        '{}:-'.format(output_format)
    ]
    proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    stdout, stderr = proc.communicate(img_bytes)
    return stdout
