"""
Implement PlantUML Text Encoding, described in http://plantuml.com/pte.

A text description has to be:
- Encoded in UTF-8
- Compressed using Deflate algorithm
- Reencoded in ASCII using a transformation "close to base64"
"""
import zlib

from six.moves import zip_longest
from six import string_types

SIXBITOFFSET = [48] * 10 + [55] * 26 + [61] * 26 + [-17] + [32]


def encode(text):
    "Apply PlantUML text encoding to a diagram description"
    assert isinstance(text, string_types)
    utf8_encoded_data = text.encode('utf-8')
    compressed_data = bytearray(zlib.compress(utf8_encoded_data)[2:-4])
    return _encode_similar_to_base64(compressed_data)


def _encode_similar_to_base64(byte_seq):
    "Encode a byte sequence 3 bytes at a time, padding with zeros"
    assert isinstance(byte_seq, bytearray)
    return ''.join(
        _encode_3_bytes(c1, c2, c3) for c1, c2, c3 in _grouper(byte_seq, 3, 0))


def _grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    assert isinstance(iterable, bytearray)
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


def _encode_3_bytes(byte1, byte2, byte3):
    "Take 3 8-bits groups and encode them as 4 6-bits groups"
    assert isinstance(byte1, int)
    assert isinstance(byte2, int)
    assert isinstance(byte3, int)
    sixbits1 = byte1 >> 2
    sixbits2 = ((byte1 & 0x3) << 4) | (byte2 >> 4)
    sixbits3 = ((byte2 & 0xF) << 2) | (byte3 >> 6)
    sixbits4 = byte3 & 0x3F
    return ''.join([
        _encode_6_bits(sixbits1 & 0x3F), _encode_6_bits(sixbits2 & 0x3F),
        _encode_6_bits(sixbits3 & 0x3F), _encode_6_bits(sixbits4 & 0x3F)
    ])


def _encode_6_bits(six_bits):
    "Encode a group of 6 bits into a charcter valid in a URL"
    assert isinstance(six_bits, int)
    return chr(SIXBITOFFSET[six_bits] + six_bits)
