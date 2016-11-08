"""Low-level wrapper around zbar's interface
"""
import platform
import sys

from ctypes import (
    addressof, byref, cdll, c_ubyte, c_char, c_char_p, c_int, c_uint, c_ulong,
    c_void_p, Structure, CFUNCTYPE, pointer, POINTER
)
from ctypes.util import find_library
from enum import IntEnum, unique
from pathlib import Path


# Types
c_ubyte_p = POINTER(c_ubyte)
c_uint_p = POINTER(c_uint)
c_ulong_p = POINTER(c_ulong)
"""unsigned char* type
"""


# Defines and enums
@unique
class ZBarSymbol(IntEnum):
    NONE        =      0  # /**< no symbol decoded */
    PARTIAL     =      1  # /**< intermediate status */
    EAN2        =      2  # /**< GS1 2-digit add-on */
    EAN5        =      5  # /**< GS1 5-digit add-on */
    EAN8        =      8  # /**< EAN-8 */
    UPCE        =      9  # /**< UPC-E */
    ISBN10      =     10  # /**< ISBN-10 (from EAN-13). @since 0.4 */
    UPCA        =     12  # /**< UPC-A */
    EAN13       =     13  # /**< EAN-13 */
    ISBN13      =     14  # /**< ISBN-13 (from EAN-13). @since 0.4 */
    COMPOSITE   =     15  # /**< EAN/UPC composite */
    I25         =     25  # /**< Interleaved 2 of 5. @since 0.4 */
    DATABAR     =     34  # /**< GS1 DataBar (RSS). @since 0.11 */
    DATABAR_EXP =     35  # /**< GS1 DataBar Expanded. @since 0.11 */
    CODABAR     =     38  # /**< Codabar. @since 0.11 */
    CODE39      =     39  # /**< Code 39. @since 0.4 */
    PDF417      =     57  # /**< PDF417. @since 0.6 */
    QRCODE      =     64  # /**< QR Code. @since 0.10 */
    CODE93      =     93  # /**< Code 93. @since 0.11 */
    CODE128     =    128  # /**< Code 128 */


@unique
class ZBarConfig(IntEnum):
    CFG_ENABLE = 0         # /**< enable symbology/feature */
    CFG_ADD_CHECK = 1      # /**< enable check digit when optional */
    CFG_EMIT_CHECK = 2     # /**< return check digit when present */
    CFG_ASCII = 3          # /**< enable full ASCII character set */
    CFG_NUM = 4            # /**< number of boolean decoder configs */

    CFG_MIN_LEN = 0x20     # /**< minimum data length for valid decode */
    CFG_MAX_LEN = 0x21     # /**< maximum data length for valid decode */

    CFG_UNCERTAINTY = 0x40 # /**< required video consistency frames */

    CFG_POSITION = 0x80    # /**< enable scanner to collect position data */

    CFG_X_DENSITY = 0x100  # /**< image scanner vertical scan density */
    CFG_Y_DENSITY = 0x101  # /**< image scanner horizontal scan density */


# Structs
class zbar_image_scanner(Structure):
    """Opaque C++ class with private implementation
    """
    pass


class zbar_image(Structure):
    """Opaque C++ class with private implementation
    """
    pass


LIBZBAR = None

def load_libzbar():
    global LIBZBAR
    if not LIBZBAR:
        sysname = platform.system()
        if 'Windows' == sysname:
            # Assume a DLL that is on sys.path. The DLL is specific to the bit
            # depth of interpreter.
            if sys.maxsize > 2**32:
                fname = 'libzbar64-0.dll'
                dependencies = ['libiconv.dll']
            else:
                fname = 'libzbar-0.dll'
                dependencies = ['libiconv-2.dll', 'zlib1.dll']

            for dir in sys.path:
                path = Path(dir).joinpath(fname)
                if path.is_file():
                    # Only try to load dependencies if the zbar DLL exists
                    try:
                        # The dependencies must be loaded first
                        for dep in dependencies:
                            cdll.LoadLibrary(str(Path(dir).joinpath(dep)))
                        LIBZBAR = cdll.LoadLibrary(str(Path(dir).joinpath(fname)))
                    except OSError as e:
                        pass
                    else:
                        # Sucessfully loaded the DLL
                        break
            else:
                raise ImportError('Unable to find zbar DLL')
        else:
            # Assume a shared library on the path.
            path = find_library('zbar')
            if not path:
                raise ImportError('Unable to find zbar shared library')
            LIBZBAR = cdll.LoadLibrary(path)

    return LIBZBAR


# Function signatures
def zbar_function(fname, restype, *args):
    """Returns a foreign function exported by `zbar`.

    Args:
        fname (:obj:`str`): Name of the exported function as string.
        restype (:obj:): Return type - one of the `ctypes` primitive C data
        types.
        *args: Arguments - a sequence of `ctypes` primitive C data types.

    Returns:
        cddl.CFunctionType: A wrapper around the function.
    """
    prototype = CFUNCTYPE(restype, *args)
    return prototype((fname, load_libzbar()))


zbar_version = zbar_function(
    'zbar_version',
    c_int,
    c_uint_p,    # major,
    c_uint_p,    # minor
)

zbar_set_verbosity = zbar_function(
    'zbar_set_verbosity',
    None,
    c_int
)

zbar_image_scanner_create = zbar_function(
    'zbar_image_scanner_create',
    POINTER(zbar_image_scanner)
)

zbar_image_scanner_destroy = zbar_function(
    'zbar_image_scanner_destroy',
    None,
    POINTER(zbar_image_scanner)
)

zbar_parse_config = zbar_function(
    'zbar_parse_config',
    c_int,
    c_char_p,          # config_string,
    POINTER(c_int),    # symbology - values in ZBarSymbol
    POINTER(c_int),    # config - values in ZBarConfig
    POINTER(c_int),    # value
)

zbar_image_scanner_set_config = zbar_function(
    'zbar_image_scanner_set_config',
    c_int,
    POINTER(zbar_image_scanner), # scanner
    c_int,                       # symbology - values in ZBarSymbol
    c_int,                       # config - values in ZBarConfig
    c_int                        # value
)

zbar_image_create = zbar_function(
    'zbar_image_create',
    POINTER(zbar_image)
)

zbar_image_destroy = zbar_function(
    'zbar_image_destroy',
    None,
    POINTER(zbar_image)
)

zbar_image_set_format = zbar_function(
    'zbar_image_set_format',
    None,
    POINTER(zbar_image),
    c_uint
)

zbar_image_set_size = zbar_function(
    'zbar_image_set_size',
    None,
    POINTER(zbar_image),
    c_uint,     # width
    c_uint      # height
)

zbar_image_set_data = zbar_function(
    'zbar_image_set_data',
    None,
    POINTER(zbar_image),
    c_void_p,   # data
    c_ulong,    # raw_image_data_length
    c_void_p    # A function pointer(!)
)

zbar_scan_image = zbar_function(
    'zbar_scan_image',
    c_int,
    POINTER(zbar_image_scanner),
    POINTER(zbar_image)
)

zbar_image_first_symbol = zbar_function(
    'zbar_image_first_symbol',
    POINTER(c_int),        # values in ZBarSymbol
    POINTER(zbar_image)
)

zbar_symbol_get_data_length = zbar_function(
    'zbar_symbol_get_data_length',
    c_uint,
    POINTER(c_int)         # values in ZBarSymbol
)

zbar_symbol_get_data = zbar_function(
    'zbar_symbol_get_data',
    c_char_p,
    POINTER(c_int)         # values in ZBarSymbol
)

zbar_symbol_next = zbar_function(
    'zbar_symbol_next',
    POINTER(c_int),
    POINTER(c_int)         # values in ZBarSymbol
)
