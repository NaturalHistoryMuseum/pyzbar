import sys
import unittest

from pathlib import Path
from contextlib import contextmanager

# TODO Would io.StringIO not work in all cases?
try:
    from cStringIO import StringIO
except ImportError:
    from io import StringIO

from pyzbar.scripts.read_zbar import main


@contextmanager
def capture_stdout():
    sys.stdout, old_stdout = StringIO(), sys.stdout
    try:
        yield sys.stdout
    finally:
        sys.stdout = old_stdout


class TestReadZbar(unittest.TestCase):
    def test_read_qrcode(self):
        "Read QR code"
        with capture_stdout() as stdout:
            main([str(Path(__file__).parent.joinpath('qrcode.png'))])

        if 2 == sys.version_info[0]:
            expected = "Thalassiodracon"
        else:
            expected = "b'Thalassiodracon'"

        self.assertEqual(expected, stdout.getvalue().strip())

    def test_read_code128(self):
        "Read CODE 128 barcodes"
        with capture_stdout() as stdout:
            main([str(Path(__file__).parent.joinpath('code128.png'))])

        if 2 == sys.version_info[0]:
            expected = "Foramenifera\nRana temporaria"
        else:
            expected = "b'Foramenifera'\nb'Rana temporaria'"

        self.assertEqual(expected, stdout.getvalue().strip())


if __name__ == '__main__':
    unittest.main()
