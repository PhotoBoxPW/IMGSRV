from PIL import Image, ImageDraw

from utils.endpoint import Endpoint, setup
from utils.textutils import render_text_with_emoji


@setup
class Achievement(Endpoint):
    def generate(self, kwargs):
        text = kwargs['text'][:24]
        challenge = False if not 'challenge' in kwargs else bool(kwargs['challenge'])
        icon_x = 13 if not 'icon_x' in kwargs else bool(kwargs['icon_x'])
        icon_y = 6 if not 'icon_y' in kwargs else bool(kwargs['icon_y'])
        color = '#fc86fc' if challenge else '#f8f628'

        if not 'header' in kwargs:
            header = 'Challenge complete!' if challenge else 'Achievement get!'
        else: header = kwargs['header'][:24]

        base = Image.open(self.get_asset('achievement.bmp')).convert('RGBA')
        font = self.assets.get_font('mc.ttf', size=24)
        canv = ImageDraw.Draw(base)
        render_text_with_emoji(base, canv, (93, 20), header, font, color)
        render_text_with_emoji(base, canv, (93, 56), text, font, 'white')

        icon = Image.open(self.get_asset('items.bmp'))
        icon = icon.crop((icon_x * 32, icon_y * 32, icon.width, icon.height))
        icon = icon.crop((0, 0, 32, 32))
        icon = icon.resize((64, 64), resample=Image.NEAREST)
        base.paste(icon, (20, 20), icon)

        return self.send_file(base)