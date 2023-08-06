#!/usr/bin/env python3

import urllib3
import codecs
import json
import re

try:
    from src import colorText
except ModuleNotFoundError:
    import colorText
try:
    from src import parseUrl
except ModuleNotFoundError:
    import parseUrl


class checkFile:
    def __init__(self, args):
        self.fileToCheck = codecs.open(args.file)
        self.secureCheck = args.secureHttp
        self.ignoreFile = args.ignoreFile
        self.telescope = args.telescope

        self.style = colorText.colourText()
        self.timeout = urllib3.Timeout(
            connect=2.5,
            read=2.5,
        )
        self.allLinks = []
        self.jsonLinks = []
        self.ignoreList = []

        try:
            if self.ignoreFile:
                self.getIgnoreList(self.ignoreFile)

            if self.telescope:
                self.makeFileFromTelescope()
        except Exception as e:
            print(f"\n{e}")

    # Main function that performs a head request on every line
    # of the file
    def checkThatFile(self):
        print("Getting status of links...")
        for line in self.fileToCheck:
            line = self.parseWebAddress(line)
            if self.doNotIgnore(line):
                self.headRequest(line)
                if self.secureCheck:
                    self.secureHttpChecker(line)

    # Parse the web address from the given line of a file
    def parseWebAddress(self, line):
        url = parseUrl.re_weburl.search(line)

        if url:
            url = url.group(0)
        elif re.match("http://localhost:", line):
            url = line

        return url

    # Gets the status of a URL response
    def headRequest(self, link):
        manager = urllib3.PoolManager(timeout=self.timeout)
        try:
            response = manager.request("HEAD", link)
            self.allLinks.append(
                {"url": link, "status": response.status, "secured": False}
            )
        except Exception:
            self.allLinks.append({"url": link, "status": "???", "secured": False})

    # Checks to see if a 'http' link will work with 'https'
    def secureHttpChecker(self, link):
        manager = urllib3.PoolManager(timeout=self.timeout)
        isHttp = re.match("(http)", link)

        if isHttp:
            link = re.sub("(http)", "https", link)
            try:
                response = manager.request("HEAD", link)
                self.allLinks.append(
                    {"url": link, "status": response.status, "secured": True}
                )
            except Exception:
                pass

    # returns false if url's domain is in ignoreList
    def doNotIgnore(self, url):
        for domain in self.ignoreList:
            if re.match(f"{domain}", url):
                return False
        return True

    # returns a list of all regex matches inside ignoreFile
    def getIgnoreList(self, ignoreFile):
        try:
            if ignoreFile:
                with open(ignoreFile) as src:
                    self.ignoreList = re.findall(
                        r"^http[s]?://.*[^\s/]", src.read(), re.MULTILINE
                    )
                    src.seek(0)
                    for line in src:
                        if re.match("#", line) or re.match("\n", line):
                            pass
                        elif re.match(r"^http[s]?://", line):
                            pass
                        else:
                            raise ValueError(
                                (
                                    "\nInvalid file format for --ignore."
                                    'Lines must start with "#", "http://", or "https://" only.'
                                )
                            )
        except FileNotFoundError:
            raise

    # Overwrites the file given with data from Telescope posts
    def makeFileFromTelescope(self):
        self.fileToCheck.close()
        self.fileToCheck = None
        self.fileToCheck = []

        baseURL = "http://localhost:3000/posts/"

        posts = self.manager.request("GET", baseURL)
        posts = json.loads(posts.data.decode("utf-8"))

        for post in posts:
            self.fileToCheck.append(f'{baseURL}{post["id"]}')

    def printAll(self):
        for line in self.allLinks:
            if line["status"] == "???":
                print(
                    (
                        f'{self.style._unknownLink}[{line["status"]}] '
                        f'{line["url"]}{self.style._plainText}'
                    )
                )
            elif line["status"] < 400 and line["secured"]:
                print(
                    (
                        f'{self.style._securedLink}[{line["status"]}] '
                        f'{line["url"]}{self.style._plainText}'
                    )
                )
            elif line["status"] < 400 and not line["secured"]:
                print(
                    f'{self.style._goodLink}[{line["status"]}] {line["url"]}{self.style._plainText}'
                )
            else:
                print(
                    f'{self.style._badLink}[{line["status"]}] {line["url"]}{self.style._plainText}'
                )

    def printAllJSON(self):
        for line in self.allLinks:
            self.jsonLinks.append({"url": line["url"], "status": line["status"]})

        print(f"{self.jsonLinks}")

    def printGoodResults(self):
        for line in self.allLinks:
            if line["status"] == "???":
                pass
            elif line["status"] < 400 and line["secured"]:
                print(
                    (
                        f'{self.style._securedLink}[{line["status"]}] '
                        f'{line["url"]}{self.style._plainText}'
                    )
                )
            elif line["status"] < 400 and not line["secured"]:
                print(
                    f'{self.style._goodLink}[{line["status"]}] {line["url"]}{self.style._plainText}'
                )

    def printGoodResultsJSON(self):
        for line in self.allLinks:
            if line["status"] == "???":
                pass
            elif line["status"] < 400:
                self.jsonLinks.append({"url": line["url"], "status": line["status"]})

        print(f"{self.jsonLinks}")

    def printBadResults(self):
        for line in self.allLinks:
            if line["status"] == "???":
                print(
                    (
                        f'{self.style._unknownLink}[{line["status"]}] '
                        f'{line["url"]}{self.style._plainText}'
                    )
                )
            elif line["status"] > 399:
                print(
                    f'{self.style._badLink}[{line["status"]}] {line["url"]}{self.style._plainText}'
                )

    def printBadResultsJSON(self):
        for line in self.allLinks:
            if line["status"] == "???":
                self.jsonLinks.append({"url": line["url"], "status": line["status"]})
            elif line["status"] > 399:
                self.jsonLinks.append({"url": line["url"], "status": line["status"]})

        print(f"{self.jsonLinks}")
