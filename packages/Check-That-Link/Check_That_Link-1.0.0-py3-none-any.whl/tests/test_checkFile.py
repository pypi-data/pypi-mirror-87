import src.checkFile as checkFile
from unittest import mock
import pytest


class Args:
    pass


args = Args()
args.file = "resources/test.html"
args.secureHttp = None
args.json = None
args.all = None
args.good = None
args.bad = None
args.ignoreFile = None
args.telescope = None


def test_no_file_exception():
    args.file = "wrong/file/path"

    with pytest.raises(FileNotFoundError):
        checkFile.checkFile(args)

    args.file = "resources/test.html"


def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, status):
            self.status = status

        def status(self):
            return self

    if args[1] == "http://google.com":
        return MockResponse(400)
    elif args[1] == "http://google.cim":
        return MockResponse(404)

    return MockResponse("???")


@mock.patch("urllib3.PoolManager.request", side_effect=mocked_requests_get)
def test_headRequest_200(self):
    link = "http://google.com"
    cF = checkFile.checkFile(args)
    cF.headRequest(link)

    assert cF.allLinks[0] == {
        "url": "http://google.com",
        "status": 400,
        "secured": False,
    }


@mock.patch("urllib3.PoolManager.request", side_effect=mocked_requests_get)
def test_headRequest_404(self):

    link = "http://google.cim"
    cF = checkFile.checkFile(args)
    cF.headRequest(link)

    assert cF.allLinks[0] == {
        "url": "http://google.cim",
        "status": 404,
        "secured": False,
    }


@mock.patch("urllib3.PoolManager.request", side_effect=mocked_requests_get)
def test_headRequest_unknown(self):

    link = ""
    cF = checkFile.checkFile(args)
    cF.headRequest(link)

    assert cF.allLinks[0] == {
        "url": "",
        "status": "???",
        "secured": False,
    }


def test_parseWebAddress():

    lineToParse = "https://www.google.com/search?q=help"

    cF = checkFile.checkFile(args)

    assert cF.parseWebAddress(lineToParse) == "https://www.google.com/search?q=help"


@mock.patch("urllib3.PoolManager.request", side_effect=mocked_requests_get)
def test_output_printAll(self, capsys):
    link = "http://google.com"
    cF = checkFile.checkFile(args)
    cF.headRequest(link)
    cF.printAll()
    captured = capsys.readouterr()
    assert captured.out == "\x1b[91m[400] http://google.com\x1b[0m\n"


@mock.patch("urllib3.PoolManager.request", side_effect=mocked_requests_get)
def test_output_printAll_unknown(self, capsys):
    link = "thisdoesnotwork"
    cF = checkFile.checkFile(args)
    cF.headRequest(link)
    cF.printAll()
    captured = capsys.readouterr()
    assert captured.out == "\x1b[90m[???] thisdoesnotwork\x1b[0m\n"


@mock.patch("urllib3.PoolManager.request", side_effect=mocked_requests_get)
def test_output_printAll_JSON_400(self, capsys):
    answer_str = "[{'url': 'http://google.com', 'status': 400}]\n"
    link = "http://google.com"
    cF = checkFile.checkFile(args)
    cF.headRequest(link)
    cF.printAllJSON()
    captured = capsys.readouterr()
    assert captured.out == answer_str
