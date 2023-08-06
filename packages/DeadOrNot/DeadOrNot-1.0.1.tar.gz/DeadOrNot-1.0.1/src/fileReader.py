import re
import sys

import requests
import threading
from colorama import Fore, init

init()


# Class to manage and store url information
class Link:
    def __init__(self, url):
        self.linkUrl = url
        self.linkStatus = None
        self.linkValid = None
        self.linkInfo = ""

    def checkStatus(self, option):

        try:
            self.linkStatus = requests.head(self.linkUrl).status_code
            if self.linkStatus == 200:
                self.linkValid = "good"
            elif self.linkStatus == 400 or self.linkStatus == 404:
                self.linkValid = "bad"
            else:
                self.linkValid = "unknown"
        except requests.exceptions.RequestException:
            self.linkValid = "unknown"
            self.linkStatus = "failed to establish a connection"
        if option == "json":
            self.linkInfo = (
                '{ "url": \''
                + self.linkUrl
                + '\', "status":'
                + str(self.linkStatus)
                + " }"
            )
        else:
            self.linkInfo = (
                self.linkUrl
                + " is a "
                + self.linkValid
                + " link with a HTTP status of "
                + str(self.linkStatus)
            )

        if self.linkStatus == 200:
            if option != "bad":
                print(Fore.GREEN + self.linkInfo)
        elif self.linkStatus == 400 or self.linkStatus == 404:
            if option != "good":
                print(Fore.RED + self.linkInfo)
        else:
            if option != "good":
                print(Fore.YELLOW + self.linkInfo)


# Class to manage and store file information
class TextFile:
    def __init__(self, filePath):
        # try to read and store file information, catch fileNotFound and IO errors
        try:
            self.fileText = open(filePath, "r").read()
            self.fileUrls = set(
                re.findall(
                    "(http|ftp|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?",
                    self.fileText,
                )
            )
            self.fileLinks = [
                Link((url[0] + "://" + url[1] + url[2])) for url in self.fileUrls
            ]
        except FileNotFoundError:
            self.fileText = None
            print("File was not found")
        except IOError:
            print("File was unable to be read")
            self.fileText = None

    def checkLinkStatuses(self, option):
        # use multithreading for http requests
        self.fileThreads = [
            threading.Thread(target=url.checkStatus(option)) for url in self.fileLinks
        ]
        for thread in self.fileThreads:
            thread.start()
        for thread in self.fileThreads:
            thread.join()

    def compareLinks(self, link, pattern):
        # try to read and store file information, catch fileNotFound and IO errors
        self.match = False
        for url in pattern:
            if re.search(url.linkUrl, link):
                self.match = re.search(url.linkUrl, link)
                break


# Class to manage and store ignore file information
class IgnoreFile:
    def __init__(self, ignoreFilePath):
        # try to read and store file information, catch fileNotFound and IO errors
        try:
            path = ignoreFilePath[0]
            self.fileText = open(path, "r").read()
            self.fileComments = set(re.findall("#.*", self.fileText))
            self.fileUrl = set(
                re.findall(
                    "(?!# )(http|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?",
                    self.fileText,
                )
            )
            self.fileInvalidUrl = set(
                re.findall(
                    "(?!# )(?!http|https)(?!://)([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?",
                    self.fileText,
                )
            )
            self.fileLink = []
            if self.fileUrl:
                self.fileLink = [
                    Link((url[0] + "://" + url[1] + url[2])) for url in self.fileUrl
                ]
            elif self.fileInvalidUrl:
                print(
                    "The URL provided is invalid. Must begin with https:// or http://"
                )
                sys.exit(-1)
        except FileNotFoundError:
            self.fileText = None
            print("File was not found")
        except IOError:
            print("File was unable to be read")
            self.fileText = None
