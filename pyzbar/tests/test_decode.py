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
            type='CODE128'
        ),
        Decoded(
            data=b'Rana temporaria',
            type='CODE128'
        )
    ]

    EXPECTED_QRCODE = [
        Decoded(
            b'Thalassiodracon',
            type='QRCODE'
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
