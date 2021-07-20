import subprocess
import pynixutil
import os.path
import typing
import pytest
import json
import os
import re


FIXTURES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures")


def camel_to_snake_case(s: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", "_", s).lower()


def assert_deepequals(a, b, _path=None):
    _path = _path if _path else tuple()
    path = ".".join(_path)
    err = ValueError("{}: {} != {}".format(path, a, b))

    def make_path(entry):
        return _path + (str(entry),)

    if isinstance(a, list):
        if not isinstance(b, list) or len(a) != len(b):
            raise err

        for vals in zip(a, b):
            p = make_path("[]")
            assert_deepequals(*vals, _path=p)

    elif isinstance(a, dict):

        for key in list(a.keys()):
            p = make_path(key)

            try:
                a_value = a[key]
            except KeyError:
                # Take backwards compat into account
                if key == "system":
                    a_value = a["platform"]
                elif key == "platform":
                    a_value = a["system"]
                else:
                    a_value = None

            try:
                b_value = b[key]
            except (TypeError, KeyError):
                try:
                    b_value = getattr(b, key)
                except AttributeError:
                    b_value = getattr(b, camel_to_snake_case(key))

            assert_deepequals(a_value, b_value, _path=p)

    elif a == b:
        return

    else:
        raise err


def drvparse_nix(drv_path: str) -> typing.Dict:
    """Parse a drv file using nix-show-derivation for comparison"""

    # Trick nix show-derivation into parsing files outside the store
    env = os.environ.copy()
    env["NIX_STORE_DIR"] = FIXTURES_DIR

    p = subprocess.run(
        ["nix", "show-derivation", drv_path],
        env=env,
        check=True,
        stdout=subprocess.PIPE,
    )
    for x in json.loads(p.stdout).values():
        return x
    raise ValueError()


def drvparse_pynixutil(drv_path: str) -> typing.Dict:
    """Parse a drv using pynixutil"""
    with open(drv_path) as f:
        return pynixutil.drvparse(f.read())


def get_fixtures() -> typing.List[str]:
    return [
        os.path.join(FIXTURES_DIR, drv_path) for drv_path in os.listdir(FIXTURES_DIR)
    ]


def test_parameters():
    drvs = get_fixtures()
    assert len(drvs) == 4


@pytest.mark.parametrize("drv", get_fixtures())
def test_parse(drv):
    """Test comparing parsing drv '%s' between nix & pynixutil""" % drv
    assert_deepequals(drvparse_nix(drv), drvparse_pynixutil(drv))
