from utils.color_ops import duotone
from PIL import Image, ImageDraw, ImageColor, ImageOps

from utils import http
from utils.endpoint import Endpoint, setup
from utils.perspective import center_content, convert_pad
from utils.textutils import render_text_with_emoji


@setup
class Wanted(Endpoint):
    def generate(self, kwargs):
        image_url = kwargs['image']
        username = kwargs['username'].upper()

        base = Image.open(self.get_asset('wanted.bmp'))

        text_layer = Image.new('RGBA', (517, 54))
        font = self.assets.get_font('edmunds.ttf', size=50)
        canv = ImageDraw.Draw(text_layer)
        render_text_with_emoji(text_layer, canv, (0, 0), username, font=font, fill='Black')
        text_layer = center_content(text_layer)
        base.paste(text_layer, (184, 962), text_layer)

        avatar = convert_pad(http.get_image(image_url), (545, 536))
        avatar_toned = ImageOps.colorize(avatar.convert('L'), black=ImageColor.getrgb('#180e04'), white=ImageColor.getrgb('#efcea3'), mid=ImageColor.getrgb('#e29f4e'))
        base.paste(avatar_toned, (166, 422), avatar)

        overlay = Image.open(self.get_asset('wanted_overlay.bmp'))
        base.paste(overlay, (0, 0), overlay)

        base = base.convert('RGB')
        return self.send_file(base, format='jpeg')
