# MIT License

# Copyright (c) 2021 Tweag IO

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import base64


_B32_ORIG = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"
_B32_NIX = "0123456789abcdfghijklmnpqrsvwxyz"
_B32_DEC_TRANS = str.maketrans(_B32_NIX, _B32_ORIG)
_B32_ENC_TRANS = bytes.maketrans(_B32_ORIG.encode(), _B32_NIX.encode())


def b32decode(s: str, **kwargs) -> bytes:
    return base64.b32decode(s.translate(_B32_DEC_TRANS), **kwargs)


def b32encode(b: bytes) -> bytes:
    return base64.b32encode(b).translate(_B32_ENC_TRANS)
