#!/usr/bin/env python
import qrcode
import uuid
import tempfile

from qrcode.image.custom_pil import PilImage
from qrcode.constants import ERROR_CORRECT_H

from page import Page
from settings import OUTPUT_DIR, PER_PAGE

default_factories = {
    'pil': 'qrcode.image.pil.PilImage',
}

version = 0
data = 'http://github.com/nimnull/qrcode'
number = '123123'
text = u'Some text to be printed below'
count = 10


def main(version, data, number, text, count):
    """ Main stub method for testing QR-code generation
    """
    qr = qrcode.QRCode(version=6, error_correction=ERROR_CORRECT_H, box_size=4)
    qr.add_data(data)
    img = qr.make_image(image_factory=PilImage, version=version,
                        qr_text=number)
    tmp_file = tempfile.TemporaryFile(suffix='.png')
    img.save(tmp_file)

    code_count = count

    while code_count > 0:
        rest = code_count - PER_PAGE
        per_page = rest >= 0 and PER_PAGE or PER_PAGE + rest
        Page(img, version, per_page, text).compose().save("%s/%s" %
            (OUTPUT_DIR.strip('/'), uuid.uuid4().hex))
        code_count = rest

    # create_paper(version=version, qr_image=img)


if __name__ == "__main__":
    main(version, data, number, text, count)
