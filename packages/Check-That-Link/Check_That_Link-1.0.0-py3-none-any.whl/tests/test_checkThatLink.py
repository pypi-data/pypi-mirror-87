import src.checkThatLink as cl
from unittest import mock
import pytest


def _args(**override):
    args = {
        "file": "resources/test.html",
        "secureHttp": False,
        "json": False,
        "all": False,
        "good": False,
        "bad": False,
        "ignoreFile": "",
        "telescope": False,
    }
    args.update(override)
    return args


path = "resources/test.html"
igpath = "resources/ignoreUrls.txt"


@pytest.mark.parametrize(
    "argv, result",
    [
        ([path, "-s"], _args(secureHttp=True)),
        ([path, "-j"], _args(json=True)),
        ([path, "-a"], _args(all=True)),
        ([path, "-g"], _args(good=True)),
        ([path, "-b"], _args(bad=True)),
        ([path, "-i", igpath], _args(ignoreFile=igpath)),
        ([path, "-t"], _args(telescope=True)),
    ],
)
def test_setupArgs(argv, result):
    assert vars(cl.setupArgs(argv)) == result
