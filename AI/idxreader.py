"""
Provide functionality to read IDX encoded files.

See http://www.fon.hum.uva.nl/praat/manual/IDX_file_format.html for a general description
of the IDX format and http://yann.lecun.com/exdb/mnist/ for a specific example
"""

__all__ = ["read"]

import struct
from array import array
from numpy import reshape


def read(filepath):
    """
    Read an IDX encoded file.

    Arguments:
        filepath -- a string representing the absolute path to the IDX file

    Returns a numpy.array representing the data
    """

    file = open(filepath, 'rb')
    data_type, dimensions = bytearray(file.read(4))[-2:]

    sizes = tuple([struct.unpack('>i', file.read(4))[0] for _ in range(dimensions)])

    if data_type == 8:
        data_type_str = "B"
    elif data_type == 9:
        data_type_str = "b"
    elif data_type == 11:
        data_type_str = "h"
    elif data_type == 12:
        data_type_str = "i"
    elif data_type == 13:
        data_type_str = "f"
    elif data_type == 14:
        data_type_str = "d"

    data = reshape(array(data_type_str, file.read()), sizes)
    return data
