#!/usr/bin/env python3

import argparse
import sys

try:
    from src import checkFile
except ModuleNotFoundError:
    import checkFile


def main():
    args = setupArgs(sys.argv[1:])

    cf = checkFile.checkFile(args)
    cf.checkThatFile()

    if args.good:
        if args.json:
            cf.printGoodResultsJSON()
        else:
            cf.printGoodResults()
    elif args.bad:
        if args.json:
            cf.printBadResultsJSON()
        else:
            cf.printBadResults()
    else:
        if args.json:
            cf.printAllJSON()
        else:
            cf.printAll()


def setupArgs(args):
    argParser = argparse.ArgumentParser()
    argParser.add_argument("file", help="file that contains links to check")
    argParser.add_argument("-v", "--version", action="version", version="%(prog)s 0.5")
    argParser.add_argument(
        "-s",
        "--secureHttp",
        dest="secureHttp",
        action="store_true",
        help="flag to check if https works on http links",
        required=False,
    )
    argParser.add_argument(
        "-j",
        "--json",
        dest="json",
        action="store_true",
        help="display output as JSON",
        required=False,
    )
    argParser.add_argument(
        "-a",
        "--all",
        action="store_true",
        help="Flag to display all links (default behavior)",
        required=False,
    )
    argParser.add_argument(
        "-g",
        "--good",
        action="store_true",
        help="Flag to display only good links",
        required=False,
    )
    argParser.add_argument(
        "-b",
        "--bad",
        action="store_true",
        help="Flag to display only bad links",
        required=False,
    )
    argParser.add_argument(
        "-i",
        "--ignore",
        action="store",
        dest="ignoreFile",
        default="",
        help="file of URL patterns to be ignored.",
    )
    argParser.add_argument(
        "-t",
        "--telescope",
        action="store_true",
        help="Will ignore the file given and instead"
        + "check the 10 latest posts to telescope",
    )
    return argParser.parse_args(args)


if __name__ == "__main__":
    main()
