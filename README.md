# pyzbar

[![Python Versions](https://img.shields.io/badge/python-2.7%2C%203.4%2C%203.5-blue.svg)](https://github.com/NaturalHistoryMuseum/pyzbar)
[![PyPI version](https://badge.fury.io/py/pyzbar.svg)](https://badge.fury.io/py/pyzbar)
[![Travis status](https://travis-ci.org/NaturalHistoryMuseum/pyzbar.svg?branch=master)](https://travis-ci.org/NaturalHistoryMuseum/pyzbar)
[![Coverage Status](https://coveralls.io/repos/github/NaturalHistoryMuseum/pyzbar/badge.svg?branch=master)](https://coveralls.io/github/NaturalHistoryMuseum/pyzbar?branch=master)

A `ctypes`-based Python wrapper around the [zbar](http://zbar.sourceforge.net/)
barcode reader.

The
[zbar](https://sourceforge.net/p/zbar/code/ci/default/tree/python/)
wrapper is stuck in Python 2.x-land.
The [zbarlight](https://github.com/Polyconseil/zbarlight/) wrapper doesn't
provide support for Windows and depends upon Pillow.
This `ctypes`-based wrapper brings `zbar` to Python 2.7 and to Python 3.4 or
greater.

## Installation

The `zbar` `DLL`s are included with the Windows Python wheels.
On other operating systems, you will need to install the `zbar` shared library.

On Mac OS X:

```
brew install zbar
```

On Linux:

```
sudo apt-get install libzbar0
```

Install this Python wrapper; use the second form to install dependencies of
the command-line scripts:

```
pip install pyzbar
pip install pyzbar[scripts]
```





## Example usage

The `decode` function accepts instances of `PIL.Image`.

```
>>> from pyzbar.pyzbar import decode
>>> from PIL import Image
>>> decode(Image.open('pyzbar/tests/code128.png'))
[Decoded(data='Stegosaurus', rect=Rect(left=5, top=6, width=96, height=95)),
 Decoded(data='Plesiosaurus', rect=Rect(left=298, top=6, width=95, height=95))]
```

It also accepts instances of `numpy.ndarray`, which might come from loading
images using [OpenCV](http://opencv.org/).

```
>>> import cv2
>>> decode(cv2.imread('pylibdmtx/tests/datamatrix.png'))
[Decoded(data='Stegosaurus', rect=Rect(left=5, top=6, width=96, height=95)),
 Decoded(data='Plesiosaurus', rect=Rect(left=298, top=6, width=95, height=95))]
```

You can also provide a tuple `(pixels, width, height)`

```
>>> image = cv2.imread('pylibdmtx/tests/datamatrix.png')
>>> height, width = image.shape[:2]
>>> decode((image.tobytes(), width, height))
[Decoded(data='Stegosaurus', rect=Rect(left=5, top=6, width=96, height=95)),
 Decoded(data='Plesiosaurus', rect=Rect(left=298, top=6, width=95, height=95))]
```


## License

`pyzbar` is distributed under the MIT license (see `LICENCE.txt`).
The `zbar` shared library is distributed under the GNU Lesser General Public
License, version 2.1 (see `zbar-LICENCE.txt`).
