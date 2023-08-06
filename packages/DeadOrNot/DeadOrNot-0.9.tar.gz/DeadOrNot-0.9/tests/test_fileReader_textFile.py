from .. import fileReader


# Test if fileNotFound error is raised and chosen output is printed
def test_fileNotFound(capsys):
    fileReader.TextFile("doesntExist.txt")
    captured = capsys.readouterr()
    assert captured.out == "File was not found\n"


def test_urlParse():
    filePath = "tests/testFile.txt"
    testUrl = "https://gist.github.com/chrispinkney/069b09d2da5b9f7b73347d13ba3c32e7.js"
    fileUrl = []
    testFile = fileReader.TextFile(filePath)
    for url in testFile.fileUrls:
        fileUrl.append(url[0] + "://" + url[1] + url[2])
    assert fileUrl[0] == testUrl


def test_linkObject_created():
    filePath = "tests/testFile.txt"
    testFile = fileReader.TextFile(filePath)
    for link in testFile.fileLinks:
        assert isinstance(link, fileReader.Link)


def test_linkObject_URL():
    filePath = "tests/testFile.txt"
    testFile = fileReader.TextFile(filePath)
    testUrl = "https://gist.github.com/chrispinkney/069b09d2da5b9f7b73347d13ba3c32e7.js"
    assert testFile.fileLinks[0].linkUrl == testUrl
