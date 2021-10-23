import platform
import unittest

from pathlib import Path

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

try:
    import imageio
except ImportError:
    imageio = None

from pyzbar import wrapper
from pyzbar.pyzbar import (
    decode, Decoded, Rect, ZBarSymbol, EXTERNAL_DEPENDENCIES, ORIENTATION_AVAILABLE
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
            orientation='UP' if ORIENTATION_AVAILABLE else None,
            quality=77,
        ),
        Decoded(
            data=b'Rana temporaria',
            type='CODE128',
            rect=Rect(left=4, top=0, width=390, height=76),
            polygon=[(4, 1), (4, 75), (394, 76), (394, 0)],
            orientation='UP' if ORIENTATION_AVAILABLE else None,
            quality=77,
        ),
    ]

    EXPECTED_CODE128_NULL_CHARACTER = [
        Decoded(
            data=b'Hello\0Goodbye',
            type='CODE128',
            rect=Rect(left=4, top=0, width=390, height=75),
            polygon=[(4, 1), (4, 75), (394, 74), (394, 0)],
            orientation="UP" if ORIENTATION_AVAILABLE else None,
            quality=76,
        ),
    ]

    EXPECTED_QRCODE = [
        Decoded(
            b'Thalassiodracon',
            type='QRCODE',
            rect=Rect(left=27, top=27, width=145, height=145),
            polygon=[(27, 27), (27, 172), (172, 172), (172, 27)],
            orientation='UP' if ORIENTATION_AVAILABLE else None,
            quality=1,
        ),
    ]

    # Two barcodes, both with same content
    EXPECTED_QRCODE_ROTATED = [
        Decoded(
            data=b'Thalassiodracon',
            type='QRCODE',
            rect=Rect(left=173, top=10, width=205, height=205),
            polygon=[(173, 113), (276, 215), (378, 113), (276, 10)],
            orientation='UP' if ORIENTATION_AVAILABLE else None,
            quality=1,
        ),
        Decoded(
            data=b'Thalassiodracon',
            type='QRCODE',
            rect=Rect(left=32, top=208, width=158, height=158),
            polygon=[(32, 352), (177, 366), (190, 222), (46, 208)],
            orientation='RIGHT' if ORIENTATION_AVAILABLE else None,
            quality=1,
        ),
    ]

    @classmethod
    def setUpClass(cls):
        cls.code128, cls.code128_null_character, cls.qrcode, cls.qrcode_rotated, cls.empty = (
            Image.open(str(TESTDATA.joinpath(fname)))
            for fname in
            ('code128.png', 'code128_null_character.png', 'qrcode.png', 'qrcode_rotated.png', 'empty.png')
        )

        cls.maxDiff = None

        # assertRaisesRegexp was a deprecated alias removed in Python 3.11
        if not hasattr(cls, 'assertRaisesRegex'):
            cls.assertRaisesRegex = cls.assertRaisesRegexp

    @classmethod
    def tearDownClass(cls):
        cls.code128 = cls.code128_null_character = cls.qrcode = cls.qrcode_rotated = cls.empty = None

    def test_decode_code128(self):
        "Read both barcodes in `code128.png`"
        res = decode(self.code128)
        self.assertEqual(self.EXPECTED_CODE128, res)

    def test_decode_code128_null_character(self):
        "Read barcode in `code128_null_character.png` containing a null character"
        res = decode(self.code128_null_character)
        self.assertEqual(self.EXPECTED_CODE128_NULL_CHARACTER, res)

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

    @unittest.skipIf(imageio is None, 'imageio not installed')
    def test_decode_imageio(self):
        "Read image using imageio"
        res = decode(imageio.imread(TESTDATA.joinpath('code128.png')))
        self.assertEqual(self.EXPECTED_CODE128, res)

    @unittest.skipIf(cv2 is None, 'OpenCV not installed')
    def test_decode_opencv(self):
        "Read image using OpenCV"
        res = decode(cv2.imread(str(TESTDATA.joinpath('code128.png'))))
        self.assertEqual(self.EXPECTED_CODE128, res)

    @patch('pyzbar.pyzbar.zbar_image_first_symbol', autospec=True)
    def test_unrecognised_symbol_type(self, zbar_image_first_symbol):
        "The type of the first symbol is not recognised"
        def zbar_image_first_symbol_set_symbol_type(image):
            symbol = wrapper.zbar_image_first_symbol(image)
            if symbol:
                symbol.contents.type = -1
            return symbol

        zbar_image_first_symbol.side_effect = zbar_image_first_symbol_set_symbol_type

        res = decode(np.asarray(self.code128))

        expected = [
            self.EXPECTED_CODE128[0]._replace(type='Unrecognised type [-1]')
        ] + self.EXPECTED_CODE128[1:]
        self.assertEqual(expected, res)

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

    @patch('pyzbar.pyzbar.zbar_image_create', autospec=True)
    def test_zbar_image_create_fail(self, zbar_image_create):
        zbar_image_create.return_value = None
        self.assertRaisesRegex(
            PyZbarError, 'Could not create zbar image', decode, self.code128
        )
        zbar_image_create.assert_called_once_with()

    @patch('pyzbar.pyzbar.zbar_image_scanner_create', autospec=True)
    def test_zbar_image_scanner_create_fail(self, zbar_image_scanner_create):
        zbar_image_scanner_create.return_value = None
        self.assertRaisesRegex(
            PyZbarError, 'Could not create image scanner', decode, self.code128
        )
        zbar_image_scanner_create.assert_called_once_with()

    @patch('pyzbar.pyzbar.zbar_scan_image', autospec=True)
    def test_zbar_scan_image_fail(self, zbar_scan_image):
        zbar_scan_image.return_value = -1
        self.assertRaisesRegex(
            PyZbarError, 'Unsupported image format', decode, self.code128
        )
        self.assertEqual(1, zbar_scan_image.call_count)

    def test_unsupported_bits_per_pixel(self):
        # 16 bits-per-pixel
        data = (list(range(3 * 3 * 2)), 3, 3)
        self.assertRaisesRegex(
            PyZbarError,
            r'Unsupported bits-per-pixel \[16\]. Only \[8\] is supported.',
            decode, data
        )
        self.assertRaises(PyZbarError, decode, data)

    def test_inconsistent_dimensions(self):
        # Ten bytes but width x height indicates nine bytes
        data = (list(range(10)), 3, 3)
        self.assertRaisesRegex(
            PyZbarError,
            (
                r'Inconsistent dimensions: image data of 10 bytes is not '
                r'divisible by \(width x height = 9\)'
            ),
            decode, data
        )


if __name__ == '__main__':
    unittest.main()
