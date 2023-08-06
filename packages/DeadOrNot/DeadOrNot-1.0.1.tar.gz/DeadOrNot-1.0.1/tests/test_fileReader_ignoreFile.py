import pytest
from .. import fileReader


def test_ignoreFileInvalid(capsys):
    filePath = ["tests/testInvalidIgnore.txt"]
    with pytest.raises(SystemExit):
        fileReader.IgnoreFile(filePath)
    captured = capsys.readouterr()
    assert (
        captured.out
        == "The URL provided is invalid. Must begin with https:// or http://\n"
    )


def test_ignoreFileValid():
    filePath = ["tests/testInvalidCommentUrl.txt"]
    testIgnore = fileReader.IgnoreFile(filePath)
    assert (
        testIgnore.fileLink[0].linkUrl == "https://www.google.com"
        or "https://www.google.com/"
    )


def test_ignoreFileComment():
    filePath = ["tests/testComment.txt"]
    testIgnore = fileReader.IgnoreFile(filePath)
    assert testIgnore.fileComments == {"# 1. Empty file, nothing will be ignored"}


# Test if fileNotFound error is raised and chosen output is printed
def test_ignoreFileNotFound(capsys):
    fileReader.IgnoreFile("doesntExist.txt")
    captured = capsys.readouterr()
    assert captured.out == "File was not found\n"
