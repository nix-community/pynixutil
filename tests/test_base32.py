import pynixutil


def test_b32decode():
    b = pynixutil.b32decode("v5sv61sszx301i0x6xysaqzla09nksnd")
    assert b == b"\xd9u\xb3\x07Z\xffF\x00\xc4\x1d7}\xa5c\xf4P\x13i\xea\xcd"


def test_encode():
    b = pynixutil.b32encode(b"\xd9u\xb3\x07Z\xffF\x00\xc4\x1d7}\xa5c\xf4P\x13i\xea\xcd")
    assert b == b"v5sv61sszx301i0x6xysaqzla09nksnd"
