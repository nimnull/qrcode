try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    import Image, ImageDraw, ImageFont

import textwrap

from settings import (INCH, RESOLUTION, HEADER_FONT, TEXT_FONT, VERSIONS,
                      PER_PAGE)

IMAGES = 5


class Page(object):
    qr_on_page = PER_PAGE
    size = (210, 297)
    border = 1
    header_font_size = 16
    text_font_size = 14

    def __init__(self, qr, version, number_of_images, text):
        assert number_of_images <= self.qr_on_page
        self.number_of_images = number_of_images
        self.pixel_border = self.border / INCH * RESOLUTION
        self.qr, self.version = qr._img, version
        paper_size = map(lambda side: int(side / (INCH * 10) * RESOLUTION),
                         self.size)
        self.paper = Image.new("RGB", paper_size, "white")
        self.draw = ImageDraw.Draw(self.paper)
        self.version = VERSIONS[version]
        self.text = text

    def compose(self):
        header_font = get_font(HEADER_FONT, self.header_font_size)
        header_text = self.version['HEADER']
        offset = self._make_header(header_text, header_font)

        text_font = get_font(TEXT_FONT, self.text_font_size)
        # text = self.version['TEXT']
        text_height = self._make_text(self.text, text_font, 32, offset)

        qr_offset = pt2px(16 * 2) + text_height
        self._place_qr(self.number_of_images, qr_offset)

        return self

    def _make_header(self, text, image_font, offset=0):
        width, height = map(lambda side: side - self.pixel_border * 2,
                            self.paper.size)

        text_size = self.draw.textsize(text, font=image_font)
        x = width / 2 - text_size[0] / 2 + self.pixel_border
        pixel_offset = pt2px(offset)

        self.draw.text((x, self.pixel_border + pixel_offset), text,
                       font=image_font, fill=self.version['HEADER_COLOR'])
        return self.pixel_border + pixel_offset + text_size[1]

    def _make_text(self, text, image_font, offset, start):
        img = make_text_box(text, image_font, 10, self.draw)
        width, height = self.paper.size

        x1 = int(width / 2 - img.size[0] / 2)
        y1 = int(pt2px(offset) + start)

        x2, y2 = x1 + img.size[0], y1 + img.size[1]

        self.paper.paste(img, (x1, y1, x2, y2))
        return y2

    def _place_qr(self, count, offset):
        qr_side = self.qr.size[0]
        x_start = self.paper.size[0] / 2 - qr_side
        y_start = offset

        lines_horizontal = [(x_start, y_start)]
        lines_vertical = [(x_start, y_start)]

        for i in xrange(count):
            if i > 0 and i % 2 != 0:
                x_pos = x_start + qr_side
            else:
                x_pos = x_start

            if i > 0 and i % 2 == 0:
                y_start += qr_side

            lines_horizontal.append((x_start, y_start + qr_side))
            lines_vertical.append((x_pos + qr_side, y_start))

            box = (x_pos, y_start, x_pos + qr_side, y_start + qr_side)
            box = map(lambda x: int(x), box)
            self.paper.paste(self.qr, box)

        for line_start in lines_horizontal:
            draw_dotted_hotizontal(self.draw, line_start,
                                   x_start + qr_side * 2)

        for line_start in lines_vertical:
            # shift = count % 2 and qr_side or 0
            y_end = y_start + qr_side  # * (count / 2) + shift
            draw_dotted_vertical(self.draw, line_start, y_end)

    def save(self, name):
        self.paper.save("{}.png".format(name))
        return self


def make_text_box(text, image_font, padding, draw):
    line_width = 4
    lines = map(lambda l: l.strip(), textwrap.dedent(text).split(';'))
    max_line = sorted(lines, key=len)[-1]
    l_size = draw.textsize(max_line, font=image_font)

    box_size = l_size[0] + padding * 4, l_size[1] * len(lines) + padding * 2
    img = Image.new("RGB", box_size, "black")

    draw = ImageDraw.Draw(img)

    draw.rectangle((line_width, line_width, box_size[0] - line_width - 1,
                   box_size[1] - line_width - 1), fill="white")

    for i, line in enumerate(lines):
        size = draw.textsize(line, font=image_font)
        x = box_size[0] - size[0] - padding
        y = padding + size[1] * i
        draw.text((x, y), line, font=image_font, fill="black")

    return img


def draw_dotted_hotizontal(draw, start, x_end, out=50):
    start = (start[0] - out, start[1])
    x_end += out

    while start[0] < x_end:
        draw.line((start, (start[0] + 10, start[1])), fill="black", width=2)
        start = (start[0] + 20, start[1])


def draw_dotted_vertical(draw, start, y_end, out=50):
    start = (start[0], start[1] - out)
    y_end += out

    while start[1] < y_end:
        draw.line((start, (start[0], start[1] + 10)), fill="black", width=2)
        start = (start[0], start[1] + 20)


def pt2px(pt):
    return pt * RESOLUTION / 72


def get_font(font, size):
    pixel_size = pt2px(size)
    return ImageFont.truetype(font, pixel_size)
