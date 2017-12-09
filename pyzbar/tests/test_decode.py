import platform
import unittest

from pathlib import Path

import numpy as np

from PIL import Image

try:
    import cv2
except ImportError:
    cv2 = None


from pyzbar.pyzbar import decode, Decoded, ZBarSymbol, EXTERNAL_DEPENDENCIES
from pyzbar.pyzbar_error import PyZbarError


TESTDATA = Path(__file__).parent


class TestDecode(unittest.TestCase):
    EXPECTED_CODE128 = [
        Decoded(
            data=b'Foramenifera',
            type='CODE128',
            location=[
                (361, 550), (37, 551), (361, 552), (37, 553),
                (361, 554), (37, 555), (361, 556), (37, 557),
                (361, 558), (37, 559), (361, 560), (37, 561),
                (361, 562), (37, 563), (361, 564), (37, 565),
                (361, 566), (37, 567), (361, 568), (37, 569),
                (361, 570), (37, 571), (361, 572), (37, 573),
                (361, 574), (37, 575), (361, 576), (37, 577),
                (361, 578), (37, 579), (361, 580), (37, 581),
                (361, 582), (37, 583), (361, 584), (37, 585),
                (361, 586), (37, 587), (361, 588), (37, 589),
                (361, 590), (37, 591), (361, 592), (37, 593),
                (361, 594), (37, 595), (361, 596), (37, 597),
                (361, 598), (37, 599), (361, 600), (37, 601),
                (361, 602), (37, 603), (361, 604), (37, 605),
                (361, 606), (37, 607), (361, 608), (37, 609),
                (361, 610), (37, 611), (361, 612), (37, 613),
                (361, 614), (37, 615), (361, 616), (37, 617),
                (361, 618), (37, 619), (361, 620), (37, 621),
                (361, 622), (37, 623), (361, 624), (37, 625),
                (361, 626)
            ]
        ),
        Decoded(
            data=b'Rana temporaria',
            type='CODE128',
            location=[
                (394, 0), (4, 1), (394, 2), (4, 3),
                (394, 4), (4, 5), (394, 6), (4, 7),
                (394, 8), (4, 9), (394, 10), (4, 11),
                (394, 12), (4, 13), (394, 14), (4, 15),
                (394, 16), (4, 17), (394, 18), (4, 19),
                (394, 20), (4, 21), (394, 22), (4, 23),
                (394, 24), (4, 25), (394, 26), (4, 27),
                (394, 28), (4, 29), (394, 30), (4, 31),
                (394, 32), (4, 33), (394, 34), (4, 35),
                (394, 36), (4, 37), (394, 38), (4, 39),
                (394, 40), (4, 41), (394, 42), (4, 43),
                (394, 44), (4, 45), (394, 46), (4, 47),
                (394, 48), (4, 49), (394, 50), (4, 51),
                (394, 52), (4, 53), (394, 54), (4, 55),
                (394, 56), (4, 57), (394, 58), (4, 59),
                (394, 60), (4, 61), (394, 62), (4, 63),
                (394, 64), (4, 65), (394, 66), (4, 67),
                (394, 68), (4, 69), (394, 70), (4, 71),
                (394, 72), (4, 73), (394, 74), (4, 75),
                (394, 76)
            ]
        )
    ]

    EXPECTED_QRCODE = [
        Decoded(
            b'Thalassiodracon',
            type='QRCODE',
            location=[(27, 27), (27, 172), (172, 172), (172, 27)]
        )
    ]

    def setUp(self):
        self.code128 = Image.open(str(TESTDATA.joinpath('code128.png')))
        self.qrcode = Image.open(str(TESTDATA.joinpath('qrcode.png')))
        self.empty = Image.open(str(TESTDATA.joinpath('empty.png')))
        self.maxDiff = None

    def tearDown(self):
        self.code128 = self.empty = self.qrcode = None

    def test_decode_code128(self):
        "Read both barcodes in `code128.png`"
        res = decode(self.code128)
        self.assertEqual(self.EXPECTED_CODE128, res)

    def test_decode_qrcode(self):
        "Read both barcodes in `qrcode.png`"
        res = decode(self.qrcode)
        self.assertEqual(self.EXPECTED_QRCODE, res)

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
        expected = []
        self.assertEqual(expected, res)

    def test_decode_numpy(self):
        "Read image using Pillow and convert to numpy.ndarray"
        res = decode(np.asarray(self.code128))
        self.assertEqual(self.EXPECTED_CODE128, res)

    @unittest.skipIf(cv2 is None, 'OpenCV not installed')
    def test_decode_opencv(self):
        "Read image using OpenCV"
        res = decode(
            cv2.imread(str(TESTDATA.joinpath('code128.png')))
        )
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


if __name__ == '__main__':
    unittest.main()
