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

from dataclasses import dataclass
from typing import (
    Optional,
    Dict,
    List,
)
import ast
import sys


__all__ = (
    "Derivation",
    "DerivationOutput",
    "drvparse",
)


@dataclass(init=False)
class DerivationOutput:
    path: str
    hash_algo: Optional[str]
    hash: Optional[str]


@dataclass(init=False)
class Derivation:
    outputs: Dict[str, DerivationOutput]

    # drv -> outputs
    input_drvs: Dict[str, List[str]]

    input_srcs: List[str]

    system: str

    builder: str

    args: List[str]

    env: Dict[str, str]

    # This was renamed in Nix 2.4
    @property
    def platform(self) -> str:
        return self.system


def drvparse(drv_path: str) -> Derivation:
    """
    Parse a derivation into a dict using a similar format as nix show-derivation
    """

    parsed = ast.parse(drv_path)

    def parse_node(node):
        if isinstance(node, ast.List):
            return [parse_node(n) for n in node.elts]
        elif isinstance(node, ast.Constant):
            return node.value
        elif isinstance(node, ast.Tuple):
            return tuple(parse_node(n) for n in node.elts)
        elif sys.version_info.minor < 8:  # < Python3.8 compat
            if isinstance(node, (ast.Str, ast.Bytes)):
                return node.s
            elif isinstance(node, ast.Num):
                return node.n
        raise ValueError(node)

    drv = Derivation()
    for field, node in zip(Derivation.__dataclass_fields__.keys(), parsed.body[0].value.args):  # type: ignore
        value = parse_node(node)
        if field == "env":
            value = dict(value)
        elif field == "input_drvs":
            value = {k: v for k, v in value}
        elif field == "outputs":
            d = {}
            for output, store_path, hash_algo, hash_hex in value:
                drv_output = DerivationOutput()
                drv_output.path = store_path
                drv_output.hash_algo = hash_algo
                drv_output.hash = hash_hex
                d[output] = drv_output
            value = d

        setattr(drv, field, value)

    return drv
