import json
import colour
import math

from PIL import Image, ImageDraw

from utils.endpoint import Endpoint, setup
from utils.textutils import wrap
from utils.perspective import autocrop

colorsdb = json.load(open('./assets/colorNames.json'))['colors']

exact_match_colors = {
    '#decade': 'Color of the Decade',
    '#facade': 'Fake Color (Perfume)',
    '#fc2929': 'Snazzah\'s Red',
    '#1ed760': 'Spotify Green',
    '#ff4500': 'Reddit Orange',
    '#ff9900': 'Amazon Orange',
    '#7289da': 'Discord Blurple',
    '#1da1f2': 'Twitter Blue',
    '#6441a4': 'Twitch Purple',
    '#ff5500': 'Soundcloud Orange',
    '#0088cc': 'Telegram Blue'
}

def color_range_lum(c, l_from, l_to, nb):
    step = (l_to - l_from) / nb
    return [colour.Color(c, luminance=l_from + (step * i)) for i in range(0, nb + 1)]

def mult_and_clamp(n):
    return max(0, min(math.floor(n * 255), 255))

@setup
class Color(Endpoint):
    def generate(self, kwargs):
        colorcode = kwargs['color']
        c = colour.Color(colorcode)

        clr_match, colorname, exact_match, distance = self.closest_named_hex(c)

        base = Image.new('RGBA', (512, 256), c.hex_l)

        font = self.assets.get_font('robotomedium.ttf', size=32)
        clrname = self.create_text(font, colorname)
        base.paste(clrname, ((base.width // 2) - (clrname.width // 2), (base.height // 2) - (clrname.height // 2)), clrname)

        sfont = self.assets.get_font('bmmini.ttf', size=16)
        clrhex = self.create_text(sfont, c.hex_l.upper(), fill='#ddd')
        base.paste(clrhex, ((base.width // 2) - (clrhex.width // 2), (base.height // 2) + (clrname.height // 2) + 10), clrhex)

        if c.luminance > 0.05:
            ldr_toblk_clrs = color_range_lum(c, c.luminance, 0, 6)
            ldr_toblk = self.create_color_ladder(sfont, ldr_toblk_clrs, c.hex_l)
            base.paste(ldr_toblk, (0, 0))

        if c.luminance < 0.95:
            ldr_towht_clrs = color_range_lum(c, 1, c.luminance, 6)
            ldr_towht = self.create_color_ladder(sfont, ldr_towht_clrs, c.hex_l)
            base.paste(ldr_towht, (base.width - ldr_towht.width, 0))

        # region rgbblock
        r, g, b = map(mult_and_clamp, c.rgb)
        rgb_block = Image.new('RGBA', (512, 30), (0, g, 0))
        rgb_w = rgb_block.width // 3

        r_block = Image.new('RGBA', (rgb_w, rgb_block.height), (r, 0, 0))
        r_name = self.create_text(sfont, f'R: {r} - {int(c.rgb[0] * 100)}%')
        r_block.paste(r_name, ((r_block.width // 2) - (r_name.width // 2), (r_block.height // 2) - (r_name.height // 2)), r_name)
        rgb_block.paste(r_block, (0, 0), r_block)

        g_name = self.create_text(sfont, f'G: {g} - {int(c.rgb[1] * 100)}%')
        rgb_block.paste(g_name, ((rgb_block.width // 2) - (g_name.width // 2), (rgb_block.height // 2) - (g_name.height // 2)), g_name)

        b_block = Image.new('RGBA', (rgb_w, rgb_block.height), (0, 0, b))
        b_name = self.create_text(sfont, f'B: {b} - {int(c.rgb[2] * 100)}%')
        b_block.paste(b_name, ((b_block.width // 2) - (b_name.width // 2), (b_block.height // 2) - (b_name.height // 2)), b_name)
        rgb_block.paste(b_block, (rgb_block.width - b_block.width, 0), b_block)

        base = base.crop((0, -rgb_block.height - 10, base.width, base.height))
        base.paste(rgb_block, (0, 0), rgb_block)
        # endregion

        # region lumblock
        h, s, l = map(mult_and_clamp, c.hsl)
        sat_col = colour.Color(c, luminance=0.5)

        hsl_block = Image.new('RGBA', (512, 30), sat_col.hex_l)
        hsl_w = hsl_block.width // 3

        hue_col = colour.Color(c, luminance=0.5, saturation=0.5)
        h_block = Image.new('RGBA', (hsl_w, hsl_block.height), hue_col.hex_l)
        h_name = self.create_text(sfont, f'Hue: {h} - {int(c.hsl[0] * 100)}%')
        h_block.paste(h_name, ((h_block.width // 2) - (h_name.width // 2), (h_block.height // 2) - (h_name.height // 2)), h_name)
        hsl_block.paste(h_block, (0, 0), h_block)

        s_name = self.create_text(sfont, f'Sat: {s} - {int(c.hsl[1] * 100)}%')
        hsl_block.paste(s_name, ((hsl_block.width // 2) - (s_name.width // 2), (hsl_block.height // 2) - (s_name.height // 2)), s_name)

        l_block = Image.new('RGBA', (hsl_w, hsl_block.height), (l, l, l))
        l_name = self.create_text(sfont, f'Lum: {l} - {int(c.hsl[2] * 100)}%')
        l_block.paste(l_name, ((l_block.width // 2) - (l_name.width // 2), (l_block.height // 2) - (l_name.height // 2)), l_name)
        hsl_block.paste(l_block, (hsl_block.width - l_block.width, 0), l_block)

        base = base.crop((0, 0, base.width, base.height + hsl_block.height + 10))
        base.paste(hsl_block, (0, base.height - hsl_block.height), hsl_block)
        # endregion

        return self.send_file(base)

    def create_text(self, font, text, fill='white', with_shadow=True):
        textwrap = wrap(font, text, 256)
        empbg = Image.new('RGBA', (512, 256))
        canv = ImageDraw.Draw(empbg)
        if with_shadow: self.text_shadow(canv, font, textwrap, x=6, y=6, align='center')
        canv.text((6, 6), textwrap, font=font, align='center', fill=fill)
        return autocrop(empbg)

    def create_text_block(self, font, text, fill='white', bg_fill='#00000033', border_width=4):
        empbg = Image.new('RGBA', (512, 256))
        canv = ImageDraw.Draw(empbg)
        self.text_shadow(canv, font, text, align='left', x=6, y=6)
        canv.text((6, 6), text, font=font, align='left', fill=fill)
        empbg = autocrop(empbg)

        bg = Image.new('RGBA', (empbg.width + (border_width * 2), empbg.height + (border_width * 2)), bg_fill)
        bg.paste(empbg, (border_width, border_width), empbg)
        return bg

    def text_shadow(self, canv, font, text, x=0, y=0, shadowcolor='black', **kwargs):
        # thin border
        canv.text((x-1, y), text, font=font, fill=shadowcolor, **kwargs)
        canv.text((x+1, y), text, font=font, fill=shadowcolor, **kwargs)
        canv.text((x, y-1), text, font=font, fill=shadowcolor, **kwargs)
        canv.text((x, y+1), text, font=font, fill=shadowcolor, **kwargs)

        # thicker border
        canv.text((x-1, y-1), text, font=font, fill=shadowcolor, **kwargs)
        canv.text((x+1, y-1), text, font=font, fill=shadowcolor, **kwargs)
        canv.text((x-1, y+1), text, font=font, fill=shadowcolor, **kwargs)
        canv.text((x+1, y+1), text, font=font, fill=shadowcolor, **kwargs)

    def closest_named_hex(self, clr):
        if clr.hex_l in exact_match_colors:
            return (
                clr.hex_l,
                exact_match_colors[clr.hex_l],
                True,
                0
            )

        r, g, b = map(mult_and_clamp, clr.rgb)
        h, s, l = map(mult_and_clamp, clr.hsl)
        ndf1 = 0
        ndf2 = 0
        ndf = 0
        cl = -1
        df = -1

        for i, c in enumerate(colorsdb):
            if '#' + c['hex'] == clr.hex_l:
                return (f"#{c['hex']}", c['name'], True, 0)
            ndf1 = pow(r - c['r'], 2)  + pow(g - c['g'], 2)  + pow(b - c['b'], 2)
            ndf2 = pow(h - c['h'], 2)  + pow(s - c['s'], 2)  + pow(l - c['l'], 2)
            ndf = ndf1 + ndf2 * 2
            if df < 0 or df > ndf:
                df = ndf
                cl = i

        if cl == -1:
            return (
                '#000000',
                'Unnamed Color',
                False,
                0
            )

        cclr = colorsdb[cl]
        return (
            f"#{cclr['hex']}",
            cclr['name'],
            False,
            df
        )

    def create_color_ladder(self, font, colors, reference, width=100, height=256, num=7):
        c_ref = colour.Color(reference)

        base = Image.new('RGBA', (width, 0))

        block_height = height // len(colors) + 1
        for i, c in enumerate(colors):
            block = Image.new('RGBA', (width, block_height), c.hex_l)
            if c_ref.hex_l != c.hex_l:
                txt = self.create_text(font, c.hex_l.upper(), fill='#bbb')
                block.paste(txt, ((block.width // 2) - (txt.width // 2), (block.height // 2) - (txt.height // 2)), txt)
            base = base.crop((0, 0, base.width, base.height + block.height))
            base.paste(block, (0, block_height * i))

        return base
