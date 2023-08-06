import pytest
import requests
from .. import fileReader


def test_link_status404(requests_mock):
    testUrl = "https://www.google.ca/"
    requests_mock.head(testUrl, status_code=404)
    testLink = fileReader.Link(testUrl)
    testLink.checkStatus("All")
    assert testLink.linkStatus == 404


def test_link_status200(requests_mock):
    testUrl = "https://www.google.ca/"
    requests_mock.head(testUrl, status_code=200)
    testLink = fileReader.Link(testUrl)
    testLink.checkStatus("All")
    assert testLink.linkStatus == 200


def test_link_exception(requests_mock):
    testUrl = "https://www.google.ca/"
    requests_mock.head(testUrl, exc=requests.exceptions.RequestException)
    testLink = fileReader.Link(testUrl)
    testLink.checkStatus("All")
    assert testLink.linkStatus == "failed to establish a connection"


def test_link_statusUnknown(requests_mock):
    testUrl = "https://www.google.ca/"
    requests_mock.head(testUrl, status_code=500)
    testLink = fileReader.Link(testUrl)
    testLink.checkStatus("All")
    assert testLink.linkValid == "unknown"


def test_message_good(requests_mock):
    testUrl = "https://www.google.ca/"
    requests_mock.head(testUrl, status_code=200)
    testLink = fileReader.Link(testUrl)
    testLink.checkStatus("All")
    assert testLink.linkInfo == (testUrl + " is a good link with a HTTP status of 200")


def test_message_bad(requests_mock):
    testUrl = "https://www.google.ca/"
    requests_mock.head(testUrl, status_code=404)
    testLink = fileReader.Link(testUrl)
    testLink.checkStatus("All")
    assert testLink.linkInfo == (testUrl + " is a bad link with a HTTP status of 404")


def test_message_json(requests_mock):
    testUrl = "https://www.google.ca/"
    requests_mock.head(testUrl, status_code=404)
    testLink = fileReader.Link(testUrl)
    testLink.checkStatus("json")
    assert testLink.linkInfo == (
        '{ "url": \'' + testUrl + '\', "status":' + str(404) + " }"
    )


def test_option_good(requests_mock, capsys):
    testUrl = "https://www.google.ca/"
    requests_mock.head(testUrl, status_code=200)
    testLink = fileReader.Link(testUrl)
    testLink.checkStatus("good")
    captured = capsys.readouterr()
    assert captured.out == (
        "\x1b[32m" + testUrl + " is a good link with a HTTP status of 200\n"
    )
    requests_mock.head(testUrl, status_code=404)
    testLink = fileReader.Link(testUrl)
    testLink.checkStatus("good")
    captured = capsys.readouterr()
    assert captured.out == ""


def test_option_bad(requests_mock, capsys):
    testUrl = "https://www.google.ca/"
    requests_mock.head(testUrl, status_code=404)
    testLink = fileReader.Link(testUrl)
    testLink.checkStatus("bad")
    captured = capsys.readouterr()
    assert captured.out == (
        "\x1b[31m" + testUrl + " is a bad link with a HTTP status of 404\n"
    )
    requests_mock.head(testUrl, status_code=200)
    testLink = fileReader.Link(testUrl)
    testLink.checkStatus("bad")
    captured = capsys.readouterr()
    assert captured.out == ""
    requests_mock.head(testUrl, status_code=500)
    testLink = fileReader.Link(testUrl)
    testLink.checkStatus("bad")
    captured = capsys.readouterr()
    assert captured.out == (
        "\x1b[33m" + testUrl + " is a unknown link with a HTTP status of 500\n"
    )
