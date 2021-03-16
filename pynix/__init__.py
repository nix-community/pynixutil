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

import typing
import base64
import ast


__all__ = (
    "b32decode",
    "b32encode",
    "drvparse",
)


_DRV_FIELDS: typing.List[str] = [
    "outputs",
    "inputDrvs",
    "inputSrcs",
    "platform",
    "builder",
    "args",
    "env",
]


_B32_ORIG = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"
_B32_NIX = "0123456789abcdfghijklmnpqrsvwxyz"
_B32_DEC_TRANS = str.maketrans(_B32_NIX, _B32_ORIG)
_B32_ENC_TRANS = bytes.maketrans(_B32_ORIG.encode(), _B32_NIX.encode())


def b32decode(s: str, **kwargs) -> bytes:
    return base64.b32decode(s.translate(_B32_DEC_TRANS), **kwargs)


def b32encode(b: bytes) -> bytes:
    return base64.b32encode(b).translate(_B32_ENC_TRANS)


def drvparse(drv: str) -> typing.Dict:
    """
    Parse a derivation into a dict using the same format as nix show-derivation
    """

    parsed = ast.parse(drv)

    def parse_node(node):
        if isinstance(node, ast.List):
            return [parse_node(n) for n in node.elts]
        elif isinstance(node, ast.Constant):
            return node.value
        elif isinstance(node, ast.Tuple):
            return tuple(parse_node(n) for n in node.elts)
        else:
            raise ValueError(node)

    ret = {}
    for field, node in zip(_DRV_FIELDS, parsed.body[0].value.args):  # type: ignore
        value = parse_node(node)
        if field == "env":
            value = dict(value)
        elif field == "inputDrvs":
            value = {k: v for k, v in value}
        elif field == "outputs":
            d = {}
            for output, store_path, hash_algo, hash_hex in value:
                v = {"path": store_path}
                if hash_algo:
                    v["hashAlgo"] = hash_algo
                if hash_hex:
                    v["hash"] = hash_hex
                d[output] = v
            value = d

        ret[field] = value
    return ret
