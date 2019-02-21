import unittest

from pathlib import Path

try:
    from unittest.mock import call, patch
except ImportError:
    # Python 2
    from mock import call, patch

from pyzbar import zbar_library


class TestLoad(unittest.TestCase):
    def setUp(self):
        self.addCleanup(patch.stopall)
        self.cdll = patch(
            'pyzbar.zbar_library.cdll', autospec=True
        ).start()
        self.find_library = patch(
            'pyzbar.zbar_library.find_library', autospec=True
        ).start()
        self.platform = patch(
            'pyzbar.zbar_library.platform', autospec=True
        ).start()
        self.windows_fnames = patch(
            'pyzbar.zbar_library._windows_fnames', autospec=True,
            return_value=('dll fname', ['dependency fname'])
        ).start()

    def test_found_non_windows(self):
        "zbar loaded ok on non-Windows platform"
        self.platform.system.return_value = 'Not windows'

        res = zbar_library.load()

        self.platform.system.assert_called_once_with()
        self.find_library.assert_called_once_with('zbar')
        self.cdll.LoadLibrary.assert_called_once_with(
            self.find_library.return_value
        )

        self.assertEqual((self.cdll.LoadLibrary.return_value, []), res)
        self.assertEqual(0, self.windows_fnames.call_count)

    def test_not_found_non_windows(self):
        "zbar not found on non-Windows platform"
        self.platform.system.return_value = 'Not windows'
        self.find_library.return_value = None

        self.assertRaises(ImportError, zbar_library.load)

        self.platform.system.assert_called_once_with()
        self.find_library.assert_called_once_with('zbar')

    def test_found_windows(self):
        "zbar found on Windows"
        self.platform.system.return_value = 'Windows'

        res = zbar_library.load()

        self.platform.system.assert_called_once_with()
        self.cdll.LoadLibrary.assert_has_calls([
            call('dependency fname'),
            call('dll fname'),
        ])
        self.assertEqual(
            (
                self.cdll.LoadLibrary.return_value,
                [self.cdll.LoadLibrary.return_value]
            ),
            res
        )

    def test_found_second_attempt_windows(self):
        "zbar found on the second attempt on Windows"
        self.platform.system.return_value = 'Windows'
        self.cdll.LoadLibrary.side_effect = [
            OSError,                # First call does not load dependent DLL
            'loaded dependency',    # Second call loads dependent DLL
            'loaded zbar',          # Third call loads dependent DLL
        ]

        res = zbar_library.load()

        self.platform.system.assert_called_once_with()
        self.cdll.LoadLibrary.assert_has_calls([
            call('dependency fname'),
            call(str(Path(zbar_library.__file__).parent.joinpath(
                'dependency fname'
            ))),
            call(str(Path(zbar_library.__file__).parent.joinpath(
                'dll fname'
            ))),
        ])

        self.assertEqual(('loaded zbar', ['loaded dependency']), res)

    def test_not_found_windows(self):
        "zbar not found on Windows"
        self.platform.system.return_value = 'Windows'
        self.cdll.LoadLibrary.side_effect = OSError

        self.assertRaises(OSError, zbar_library.load)

        self.platform.system.assert_called_once_with()
        # Two attempts at loading
        self.cdll.LoadLibrary.assert_has_calls([
            call('dependency fname'),
            call(str(Path(zbar_library.__file__).parent.joinpath(
                'dependency fname'
            ))),
        ])


class TestWindowsFnames(unittest.TestCase):
    def setUp(self):
        self.addCleanup(patch.stopall)
        self.sys = patch('pyzbar.zbar_library.sys', autospec=True).start()

    def test_32bit(self):
        self.sys.maxsize = 2**32
        self.assertEqual(
            ('libzbar-32.dll', ['libiconv-2.dll']),
            zbar_library._windows_fnames()
        )

    def test_64bit(self):
        # This is a 'long' on a 32-bit interpreter
        self.sys.maxsize = 2**32 + 1
        self.assertEqual(
            ('libzbar-64.dll', ['libiconv.dll']),
            zbar_library._windows_fnames()
        )


if __name__ == '__main__':
    unittest.main()
