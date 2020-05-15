import platform
import unittest

from pathlib import Path

from pyzbar.locations import Point

try:
    from unittest.mock import patch
except ImportError:
    # Python 2
    from mock import patch

import numpy as np

from PIL import Image

try:
    import cv2
except ImportError:
    cv2 = None

from pyzbar.pyzbar import (
    decode, Decoded, Rect, ZBarSymbol, EXTERNAL_DEPENDENCIES
)
from pyzbar.pyzbar_error import PyZbarError

TESTDATA = Path(__file__).parent


class TestDecode(unittest.TestCase):
    EXPECTED_CODE128 = [
        Decoded(
            data=b'Foramenifera',
            type='CODE128',
            rect=Rect(left=37, top=550, width=324, height=76),
            polygon=[(37, 551), (37, 625), (361, 626), (361, 550)],
            points=[(361, 550), (37, 551), (361, 552), (37, 553), (361, 554), (37, 555), (361, 556), (37, 557),
                    (361, 558), (37, 559), (361, 560), (37, 561), (361, 562), (37, 563), (361, 564), (37, 565),
                    (361, 566), (37, 567), (361, 568), (37, 569), (361, 570), (37, 571), (361, 572), (37, 573),
                    (361, 574), (37, 575), (361, 576), (37, 577), (361, 578), (37, 579), (361, 580), (37, 581),
                    (361, 582), (37, 583), (361, 584), (37, 585), (361, 586), (37, 587), (361, 588), (37, 589),
                    (361, 590), (37, 591), (361, 592), (37, 593), (361, 594), (37, 595), (361, 596), (37, 597),
                    (361, 598), (37, 599), (361, 600), (37, 601), (361, 602), (37, 603), (361, 604), (37, 605),
                    (361, 606), (37, 607), (361, 608), (37, 609), (361, 610), (37, 611), (361, 612), (37, 613),
                    (361, 614), (37, 615), (361, 616), (37, 617), (361, 618), (37, 619), (361, 620), (37, 621),
                    (361, 622), (37, 623), (361, 624), (37, 625), (361, 626)]
        ),
        Decoded(
            data=b'Rana temporaria',
            type='CODE128',
            rect=Rect(left=4, top=0, width=390, height=76),
            polygon=[(4, 1), (4, 75), (394, 76), (394, 0)],
            points=[(394, 0), (4, 1), (394, 2), (4, 3), (394, 4), (4, 5), (394, 6), (4, 7), (394, 8), (4, 9), (394, 10),
                    (4, 11), (394, 12), (4, 13), (394, 14), (4, 15), (394, 16), (4, 17), (394, 18), (4, 19), (394, 20),
                    (4, 21), (394, 22), (4, 23), (394, 24), (4, 25), (394, 26), (4, 27), (394, 28), (4, 29), (394, 30),
                    (4, 31), (394, 32), (4, 33), (394, 34), (4, 35), (394, 36), (4, 37), (394, 38), (4, 39), (394, 40),
                    (4, 41), (394, 42), (4, 43), (394, 44), (4, 45), (394, 46), (4, 47), (394, 48), (4, 49), (394, 50),
                    (4, 51), (394, 52), (4, 53), (394, 54), (4, 55), (394, 56), (4, 57), (394, 58), (4, 59), (394, 60),
                    (4, 61), (394, 62), (4, 63), (394, 64), (4, 65), (394, 66), (4, 67), (394, 68), (4, 69), (394, 70),
                    (4, 71), (394, 72), (4, 73), (394, 74), (4, 75), (394, 76)]
        )
    ]

    EXPECTED_QRCODE = [
        Decoded(
            b'Thalassiodracon',
            type='QRCODE',
            rect=Rect(left=27, top=27, width=145, height=145),
            polygon=[(27, 27), (27, 172), (172, 172), (172, 27)],
            points=[(27, 27), (27, 172), (172, 172), (172, 27)]
        )
    ]

    # Two barcodes, both with same content
    EXPECTED_QRCODE_ROTATED = [
        Decoded(
            data=b'Thalassiodracon',
            type='QRCODE',
            rect=Rect(left=173, top=10, width=205, height=205),
            polygon=[(173, 113), (276, 215), (378, 113), (276, 10)],
            points=[(276, 10), (173, 113), (276, 215), (378, 113)]),
        Decoded(
            data=b'Thalassiodracon',
            type='QRCODE',
            rect=Rect(left=32, top=208, width=158, height=158),
            polygon=[(32, 352), (177, 366), (190, 222), (46, 208)],
            points=[(190, 222), (46, 208), (32, 352), (177, 366)])
    ]

    def setUp(self):
        self.code128, self.qrcode, self.qrcode_rotated, self.empty = (
            Image.open(str(TESTDATA.joinpath(fname)))
            for fname in
            ('code128.png', 'qrcode.png', 'qrcode_rotated.png', 'empty.png')
        )
        self.maxDiff = None

    def tearDown(self):
        self.code128 = self.empty = self.qrcode = None

    def test_decode_code128(self):
        "Read both barcodes in `code128.png`"
        res = decode(self.code128)
        self.assertEqual(self.EXPECTED_CODE128, res)

    def test_decode_qrcode(self):
        "Read barcode in `qrcode.png`"
        res = decode(self.qrcode)
        self.assertEqual(self.EXPECTED_QRCODE, res)

    def test_decode_qrcode_rotated(self):
        "Read barcode in `qrcode_rotated.png`"
        # Test computation of the polygon around the barcode
        res = decode(self.qrcode_rotated)
        self.assertEqual(self.EXPECTED_QRCODE_ROTATED, res)

    def test_symbols(self):
        "Read only qrcodes in `qrcode.png`"
        res = decode(self.qrcode, symbols=[ZBarSymbol.QRCODE])
        self.assertEqual(self.EXPECTED_QRCODE, res)

    def test_symbols_not_present(self):
        "Read only code128 in `qrcode.png`"
        res = decode(self.qrcode, symbols=[ZBarSymbol.CODE128])
        self.assertEqual([], res)

    def test_decode_tuple(self):
        "Read barcodes in pixels"
        pixels = self.code128.copy().convert('L').tobytes()
        width, height = self.code128.size
        res = decode((pixels, width, height))
        self.assertEqual(self.EXPECTED_CODE128, res)

    def test_unsupported_bpp(self):
        pixels = self.code128.tobytes()
        width, height = self.code128.size
        self.assertRaises(PyZbarError, decode, (pixels, width, height))

    def test_empty(self):
        "Do not show any output for an image that does not contain a barcode"
        res = decode(self.empty)
        self.assertEqual([], res)

    def test_decode_numpy(self):
        "Read image using Pillow and convert to numpy.ndarray"
        res = decode(np.asarray(self.code128))
        self.assertEqual(self.EXPECTED_CODE128, res)

    @unittest.skipIf(cv2 is None, 'OpenCV not installed')
    def test_decode_opencv(self):
        "Read image using OpenCV"
        res = decode(cv2.imread(str(TESTDATA.joinpath('code128.png'))))
        self.assertEqual(self.EXPECTED_CODE128, res)

    def test_external_dependencies(self):
        "External dependencies"
        if 'Windows' == platform.system():
            self.assertEqual(2, len(EXTERNAL_DEPENDENCIES))
            self.assertTrue(
                any('libiconv' in d._name for d in EXTERNAL_DEPENDENCIES)
            )
        self.assertTrue(
            any('libzbar' in d._name for d in EXTERNAL_DEPENDENCIES)
        )

    @patch('pyzbar.pyzbar.zbar_image_create')
    def test_zbar_image_create_fail(self, zbar_image_create):
        zbar_image_create.return_value = None
        self.assertRaisesRegexp(
            PyZbarError, 'Could not create zbar image', decode, self.code128
        )
        zbar_image_create.assert_called_once_with()

    @patch('pyzbar.pyzbar.zbar_image_scanner_create')
    def test_zbar_image_scanner_create_fail(self, zbar_image_scanner_create):
        zbar_image_scanner_create.return_value = None
        self.assertRaisesRegexp(
            PyZbarError, 'Could not create image scanner', decode, self.code128
        )
        zbar_image_scanner_create.assert_called_once_with()

    @patch('pyzbar.pyzbar.zbar_scan_image')
    def test_zbar_scan_image_fail(self, zbar_scan_image):
        zbar_scan_image.return_value = -1
        self.assertRaisesRegexp(
            PyZbarError, 'Unsupported image format', decode, self.code128
        )
        self.assertEqual(1, zbar_scan_image.call_count)

    def test_unsupported_bits_per_pixel(self):
        # 16 bits-per-pixel
        data = (list(range(3 * 3 * 2)), 3, 3)
        self.assertRaisesRegexp(
            PyZbarError,
            r'Unsupported bits-per-pixel \[16\]. Only \[8\] is supported.',
            decode, data
        )
        self.assertRaises(PyZbarError, decode, data)

    def test_inconsistent_dimensions(self):
        # Ten bytes but width x height indicates nine bytes
        data = (list(range(10)), 3, 3)
        self.assertRaisesRegexp(
            PyZbarError,
            (
                r'Inconsistent dimensions: image data of 10 bytes is not '
                r'divisible by \(width x height = 9\)'
            ),
            decode, data
        )


if __name__ == '__main__':
    unittest.main()
