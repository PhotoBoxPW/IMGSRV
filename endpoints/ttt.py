from PIL import Image, ImageDraw

from utils import http
from utils.endpoint import Endpoint, setup
from utils.perspective import convert_fit
from utils.textutils import render_text_with_emoji, wrap


@setup
class TTT(Endpoint):
    def generate(self, kwargs):
        image_url = kwargs['avatar']
        username = kwargs['username']
        text = kwargs['text']

        base = Image.open(self.get_asset('ttt.bmp'))
        font = self.assets.get_font('tahoma.ttf', size=11)
        canv = ImageDraw.Draw(base)

        render_text_with_emoji(base, canv, (12, 10), wrap(font, 'Body Search Results - ' + username, 305), font=font, fill='#dddddd')
        render_text_with_emoji(base, canv, (108, 130), wrap(font, "Something tells you some of this person\'s last words were: '" + text + "'--.", 279), font=font, fill='#dddddd')

        avatar = convert_fit(http.get_image(image_url), (32, 32))
        base.paste(avatar, (32, 56), avatar)

        return self.send_file(base)
