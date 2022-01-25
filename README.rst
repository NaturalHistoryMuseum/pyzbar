pyzbar
======

.. image:: https://img.shields.io/badge/python-2.7%2C%203.5%2C%203.6%2C%203.7%2C%203.8%2C%203.9%2C%203.10-blue.svg
    :target: https://github.com/NaturalHistoryMuseum/pyzbar

.. image:: https://badge.fury.io/py/pyzbar.svg
    :target: https://pypi.python.org/pypi/pyzbar

.. image:: https://img.shields.io/github/workflow/status/NaturalHistoryMuseum/pyzbar/Tests/master?label=tests
    :target: https://github.com/NaturalHistoryMuseum/pyzbar/actions?query=workflow%3A%22Tests%22

.. image:: https://coveralls.io/repos/github/NaturalHistoryMuseum/pyzbar/badge.svg?branch=master
    :target: https://coveralls.io/github/NaturalHistoryMuseum/pyzbar?branch=master

Read one-dimensional barcodes and QR codes from Python 2 and 3 using the
`zbar <http://zbar.sourceforge.net/>`__ library.

-  Pure python
-  Works with PIL / Pillow images, OpenCV / imageio / numpy ``ndarray``\ s, and raw bytes
-  Decodes locations of barcodes
-  No dependencies, other than the zbar library itself
-  Tested on Python 2.7, and Python 3.5 to 3.10

The older `zbar <https://sourceforge.net/p/zbar/code/ci/default/tree/python/>`__
package is stuck in Python 2.x-land.
The `zbarlight <https://github.com/Polyconseil/zbarlight/>`__ package does not
provide support for Windows and depends upon Pillow.

Installation
------------

The ``zbar`` DLLs are included with the Windows Python wheels.
On other operating systems, you will need to install the ``zbar`` shared
library.

Mac OS X:

::

   brew install zbar
   
or

::

   conda install -c conda-forge zbar


Linux:

::

   sudo apt-get install libzbar0

Install this Python wrapper; use the second form to install dependencies of the
command-line scripts:

::

   pip install pyzbar
   pip install pyzbar[scripts]

Example usage
-------------

The ``decode`` function accepts instances of ``PIL.Image``.

::

   >>> from pyzbar.pyzbar import decode
   >>> from PIL import Image
   >>> decode(Image.open('pyzbar/tests/code128.png'))
   [
       Decoded(
           data=b'Foramenifera', type='CODE128',
           rect=Rect(left=37, top=550, width=324, height=76),
           polygon=[
               Point(x=37, y=551), Point(x=37, y=625), Point(x=361, y=626),
               Point(x=361, y=550)
           ],
           orientation="UP",
           quality=77
       )
       Decoded(
           data=b'Rana temporaria', type='CODE128',
           rect=Rect(left=4, top=0, width=390, height=76),
           polygon=[
               Point(x=4, y=1), Point(x=4, y=75), Point(x=394, y=76),
               Point(x=394, y=0)
           ],
           orientation="UP",
           quality=77
       )
   ]

It also accepts instances of ``numpy.ndarray``, which might come from loading
images using `OpenCV <http://opencv.org/>`__.

::

   >>> import cv2
   >>> decode(cv2.imread('pyzbar/tests/code128.png'))
   [
       Decoded(
           data=b'Foramenifera', type='CODE128',
           rect=Rect(left=37, top=550, width=324, height=76),
           polygon=[
               Point(x=37, y=551), Point(x=37, y=625), Point(x=361, y=626),
               Point(x=361, y=550)
           ],
           orientation="UP",
           quality=77
       )
       Decoded(
           data=b'Rana temporaria', type='CODE128',
           rect=Rect(left=4, top=0, width=390, height=76),
           polygon=[
               Point(x=4, y=1), Point(x=4, y=75), Point(x=394, y=76),
               Point(x=394, y=0)
           ],
           orientation="UP",
           quality=77
       )
   ]

You can also provide a tuple ``(pixels, width, height)``, where the image data
is eight bits-per-pixel.

::

   >>> image = cv2.imread('pyzbar/tests/code128.png')
   >>> height, width = image.shape[:2]

   >>> # 8 bpp by considering just the blue channel
   >>> decode((image[:, :, 0].astype('uint8').tobytes(), width, height))
   [
       Decoded(
           data=b'Foramenifera', type='CODE128',
           rect=Rect(left=37, top=550, width=324, height=76),
           polygon=[
               Point(x=37, y=551), Point(x=37, y=625), Point(x=361, y=626),
               Point(x=361, y=550)
           ],
           orientation="UP",
           quality=77
       )
       Decoded(
           data=b'Rana temporaria', type='CODE128',
           rect=Rect(left=4, top=0, width=390, height=76),
           polygon=[
               Point(x=4, y=1), Point(x=4, y=75), Point(x=394, y=76),
               Point(x=394, y=0)
           ],
           orientation="UP",
           quality=77
       )
   ]

   >>> # 8 bpp by converting image to greyscale
   >>> grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
   >>> decode((grey.tobytes(), width, height))
   [
       Decoded(
           data=b'Foramenifera', type='CODE128',
           rect=Rect(left=37, top=550, width=324, height=76),
           polygon=[
               Point(x=37, y=551), Point(x=37, y=625), Point(x=361, y=626),
               Point(x=361, y=550)
           ],
           orientation="UP",
           quality=77
       )
       Decoded(
           data=b'Rana temporaria', type='CODE128',
           rect=Rect(left=4, top=0, width=390, height=76),
           polygon=[
               Point(x=4, y=1), Point(x=4, y=75), Point(x=394, y=76),
               Point(x=394, y=0)
           ],
           orientation="UP",
           quality=77
       )
   ]

   >>> # If you don't provide 8 bpp
   >>> decode((image.tobytes(), width, height))
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
     File "/Users/lawh/projects/pyzbar/pyzbar/pyzbar.py", line 102, in decode
       raise PyZbarError('Unsupported bits-per-pixel [{0}]'.format(bpp))
   pyzbar.pyzbar_error.PyZbarError: Unsupported bits-per-pixel [24]

The default behaviour is to decode all symbol types. You can look for just your
symbol types

::

   >>> from pyzbar.pyzbar import ZBarSymbol
   >>> # Look for just qrcode
   >>> decode(Image.open('pyzbar/tests/qrcode.png'), symbols=[ZBarSymbol.QRCODE])
   [
       Decoded(
           data=b'Thalassiodracon', type='QRCODE',
           rect=Rect(left=27, top=27, width=145, height=145),
           polygon=[
               Point(x=27, y=27), Point(x=27, y=172), Point(x=172, y=172),
               Point(x=172, y=27)
           ],
           orientation="UP",
           quality=1
       )
   ]


   >>> # If we look for just code128, the qrcodes in the image will not be detected
   >>> decode(Image.open('pyzbar/tests/qrcode.png'), symbols=[ZBarSymbol.CODE128])
   []

ZBar versions
-------------

Development of the `original zbar <http://zbar.sourceforge.net/>`__ stopped in 2012.
Development was started again in 2019 under a `new project <https://github.com/mchehab/zbar/>`__
that has added some new features, including support for decoding
barcode orientation. At the time of writing this new project does not produce Windows DLLs.
The ``zbar`` DLLs that are included with the Windows Python wheels are built from the original
project and so do not include support for decoding barcode orientation.
If you see ``orientation=None`` then your system has an older release of zbar that does
not support orientation.

Quality field
-------------
From
`zbar.h <https://sourceforge.net/p/zbar/code/ci/default/tree/include/zbar.h#l359>`__, the quality field is

  ...an unscaled, relative quantity: larger values are better than smaller
  values, where "large" and "small" are application dependent. Expect the exact
  definition of this quantity to change as the metric is refined. currently,
  only the ordered relationship between two values is defined and will remain
  stable in the future

Bounding boxes and polygons
---------------------------

The blue and pink boxes show ``rect`` and ``polygon``, respectively, for
barcodes in ``pyzbar/tests/qrcode.png`` (see
`bounding_box_and_polygon.py <https://github.com/NaturalHistoryMuseum/pyzbar/blob/master/bounding_box_and_polygon.py>`__).

.. figure:: https://github.com/NaturalHistoryMuseum/pyzbar/raw/master/bounding_box_and_polygon.png
   :alt: Two barcodes with bounding boxes and polygons

Windows error message
---------------------

If you see an ugly ``ImportError`` when importing ``pyzbar`` on Windows
you will most likely need the `Visual C++ Redistributable Packages for Visual
Studio 2013
<https://www.microsoft.com/en-US/download/details.aspx?id=40784>`__.
Install ``vcredist_x64.exe`` if using 64-bit Python, ``vcredist_x86.exe`` if
using 32-bit Python.

Contributors
------------

-  Alex (@globophobe) - first implementation of barcode locations
-  Dmytro Ferens (@dferens) - barcode orientation
-  Ismail Bento (@isman7) - support for images loaded using imageio
-  @jaant - read barcodes containing null characters

License
-------

``pyzbar`` is distributed under the MIT license (see ``LICENCE.txt``).
The ``zbar`` shared library is distributed under the
`GNU Lesser General Public License, version 2.1 <http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html>`__
