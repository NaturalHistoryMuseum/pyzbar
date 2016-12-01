from __future__ import print_function

from collections import namedtuple
from contextlib import contextmanager
from ctypes import cast, c_void_p, string_at

from .pyzbar_error import PyZbarError
from .wrapper import (
    zbar_image_scanner_set_config,
    zbar_image_scanner_create, zbar_image_scanner_destroy,
    zbar_image_create, zbar_image_destroy, zbar_image_set_format,
    zbar_image_set_size, zbar_image_set_data, zbar_scan_image,
    zbar_image_first_symbol, zbar_symbol_get_data,
    zbar_symbol_next, ZBarConfig, ZBarSymbol, EXTERNAL_DEPENDENCIES
)

__all__ = ['decode', 'EXTERNAL_DEPENDENCIES']


# Results of reading a barcode
Decoded = namedtuple('Decoded', ['data', 'type'])

# ZBar's magic 'fourcc' numbers that represent image formats
FOURCC = {
    'L800': 808466521,
    'GRAY': 1497715271
}


@contextmanager
def zbar_image():
    """A context manager for `zbar_image`, created and destoyed by
    `zbar_image_create` and `zbar_image_destroy`.

    Args:

    Yields:
        zbar_image: The created image

    Raises:
        PyZbarError: If the image could not be created.
    """
    image = zbar_image_create()
    if not image:
        raise PyZbarError('Could not create image')
    else:
        try:
            yield image
        finally:
            zbar_image_destroy(image)


@contextmanager
def zbar_image_scanner():
    """A context manager for `zbar_image_scanner`, created and destroyed by
    `zbar_image_scanner_create` and `zbar_image_scanner_destroy`.

    Args:

    Yields:
        zbar_image_scanner: The created scanner

    Raises:
        PyZbarError: If the decoder could not be created.
    """
    scanner = zbar_image_scanner_create()
    if not scanner:
        raise PyZbarError('Could not create decoder')
    else:
        try:
            yield scanner
        finally:
            zbar_image_scanner_destroy(scanner)


def decode(image, symbols=None):
    """Decodes datamatrix barcodes in `image`.

    Args:
        image: `numpy.ndarray`, `PIL.Image` or tuple (pixels, width, height)
        symbols (ZBarSymbol): the symbol types to decode; if `None`, use
            `zbar`'s default behaviour, which (I think) is to decode all
            symbol types.

    Returns:
        :obj:`list` of :obj:`Decoded`: The values decoded from barcodes.
    """

    # Test for PIL.Image and numpy.ndarray without requiring that cv2 or PIL
    # are installed.
    if 'PIL.' in str(type(image)):
        if 'L' != image.mode:
            image = image.convert('L')
        pixels = image.tobytes()
        width, height = image.size
    elif 'numpy.ndarray' in str(type(image)):
        if 3 == len(image.shape):
            # Take just the first channel
            image = image[:, :, 0]
        if 'uint8' != str(image.dtype):
            image = image.astype('uint8')
        try:
            pixels = image.tobytes()
        except AttributeError:
            # `numpy.ndarray.tobytes()` introduced in `numpy` 1.9.0 - use the
            # older `tostring` method.
            pixels = image.tostring()
        height, width = image.shape[:2]
    else:
        # image should be a tuple (pixels, width, height)
        pixels, width, height = image

    # Compute bits-per-pixel
    bpp = 8 * len(pixels) / (width * height)
    if 8 != bpp:
        raise PyZbarError('Unsupported bits-per-pixel [{0}]'.format(bpp))

    results = []
    with zbar_image_scanner() as scanner:
        if symbols:
            # Disable all but the symbols of interest
            disable = set(ZBarSymbol).difference(symbols)
            for symbol in disable:
                zbar_image_scanner_set_config(
                    scanner, symbol, ZBarConfig.CFG_ENABLE, 0
                )
            # I think it likely that zbar will detect all symbol types by
            # default, in which case enabling the types of interest is
            # redundant but it seems sensible to be over-cautious and enable
            # them.
            for symbol in symbols:
                zbar_image_scanner_set_config(
                    scanner, symbol, ZBarConfig.CFG_ENABLE, 1
                )
        with zbar_image() as img:
            zbar_image_set_format(img, FOURCC['L800'])
            zbar_image_set_size(img, width, height)
            zbar_image_set_data(img, cast(pixels, c_void_p), len(pixels), None)
            decoded = zbar_scan_image(scanner, img)
            if decoded < 0:
                raise PyZbarError('Unsupported image format')
            else:
                symbol = zbar_image_first_symbol(img)
                while symbol:
                    data = string_at(zbar_symbol_get_data(symbol))
                    symbol_type = ZBarSymbol(symbol.contents.value).name
                    results.append(Decoded(
                        data=data,
                        type=symbol_type
                    ))

                    symbol = zbar_symbol_next(symbol)

    return results
