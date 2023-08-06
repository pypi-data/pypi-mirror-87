import argparse
import fileReader
import threading
import sys
from termcolor import colored
import colorama


parser = argparse.ArgumentParser(
    description="Determine status of link in file",
    epilog="""The CLI takes a file path (relative or absolute)
                                        and reads and parses it for urls to check their http status""",
)

# take file names as an argument on command line
parser.add_argument("files", nargs="+")
# create command line option to output live links only
parser.add_argument("-g", "--good", action="store_true", help="Outputs only live links")
# create command line option to output dead and unknown status links only
parser.add_argument("-b", "--bad", action="store_true", help="Outputs only dead links")
# create command line option to output all links
parser.add_argument("-a", "--all", action="store_true", help="Outputs all links")
# create command line option for general information
parser.add_argument(
    "-in",
    "--info",
    action="store_true",
    help="Outputs overall information about links in file, i.e how many live or dead links there are",
)
# create command line option to output in JSON format
parser.add_argument(
    "-j", "--json", action="store_true", help="Outputs links in json format"
)
# create command line option to ignore specified link patterns
parser.add_argument(
    "-i",
    "--ignore",
    nargs=1,
    help="Outputs the links that do not match the provided pattern",
)


def processFile(file, option):
    colorama.init()
    urlFile = fileReader.TextFile(file)
    processLinks(file, urlFile, option)


def processFileWithIgnore(file, pattern, option):
    colorama.init()
    urlFile = fileReader.TextFile(file)
    for link in urlFile.fileLinks:
        urlFile.compareLinks(link.linkUrl, pattern)
        if urlFile.match:
            urlFile.fileLinks.remove(link)
    processLinks(file, urlFile, option)


def processLinks(file, urlFile, option):
    if urlFile.fileText is not None:
        urlFile.checkLinkStatuses(option)
    # info option, get counts for link status types
    if option == "info":
        deadLinks = 0
        liveLinks = 0
        unknownLinks = 0
        for url in urlFile.fileLinks:
            if url.linkValid == "good":
                liveLinks += 1
            if url.linkValid == "unknown":
                unknownLinks += 1
            if url.linkValid == "bad":
                deadLinks += 1
        print(
            "The file "
            + file
            + " has "
            + colored(str(deadLinks) + " dead links ", "red")
            + " and "
            + colored(str(liveLinks) + " live links", "green")
        )
        print(
            "There are also " + colored(str(unknownLinks) + " unknown links", "yellow")
        )


# take command line files and create thread for each file
def processArguments(argsNormal, option):
    for arg in argsNormal:
        threading.Thread(target=processFile(arg, option)).start()


# take command line files and create thread for each file, while ignoring specified links
def processArgumentsWithIgnore(argsWithIgnore, pattern, option):
    for arg in argsWithIgnore:
        threading.Thread(target=processFileWithIgnore(arg, pattern, option)).start()


if __name__ == "__main__":
    # run argparse -help option if no arguments entered on command line
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)


def filterArguments(args):
    if args.ignore:
        ignoreFile = fileReader.IgnoreFile(args.ignore)
        if args.good:
            processArgumentsWithIgnore(args.files, ignoreFile.fileLink, "good")
        elif args.bad:
            processArgumentsWithIgnore(args.files, ignoreFile.fileLink, "bad")
        elif args.info:
            processArgumentsWithIgnore(args.files, ignoreFile.fileLink, "info")
        elif args.json:
            processArgumentsWithIgnore(args.files, ignoreFile.fileLink, "json")
        else:
            processArgumentsWithIgnore(args.files, ignoreFile.fileLink, "all")
    else:
        if args.good:
            processArguments(args.files, "good")
        elif args.bad:
            processArguments(args.files, "bad")
        elif args.info:
            processArguments(args.files, "info")
        elif args.json:
            processArguments(args.files, "json")
        else:
            processArguments(args.files, "all")


# parse arguments
args = parser.parse_args()
filterArguments(args)
