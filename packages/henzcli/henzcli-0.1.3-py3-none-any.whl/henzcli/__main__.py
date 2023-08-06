import requests
import sys
from bs4 import BeautifulSoup
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), "../.env")
load_dotenv(dotenv_path)
# support color/noncolored from env
if os.environ.get("CLICOLOR") is None:
    CLICOLOR = True
else:
    CLICOLOR = os.environ.get("CLICOLOR") == "1" or os.environ.get("CLICOLOR") == 1


def main():
    # support colored print statements
    noColor = "\033[0m"
    redColor = "\033[91m"
    greenColor = "\033[92m"
    dgrayColor = "\033[90m"
    purpleColor = "\033[95m"
    # parsing arguements
    args = sys.argv[1:]
    # support help
    if len(args) < 1:
        print("HenZCLI tool is used for checking healthy links in HTML file")
        print("Basic usage as follow\n")
        print("\thenzcli <path to html file> <another file>\n")
    else:
        # support good/bad/all flag
        allIncluded = goodBad(args[0])
        # support version
        if args[0] == "-v" or args[0] == "--version":
            print("HenZCLI version 0.1")
        print("passed argument :: {}".format(args))
        for arg in args:
            validFile = fileValidation(arg)
            if validFile == 0:
                try:
                    f = open(arg, "r")
                    if CLICOLOR:
                        print(purpleColor + "In file " + arg + noColor)
                    else:
                        print("In file " + arg)
                    # parse html file
                    html = BeautifulSoup(f, "html.parser")
                    # look for all link in a tags
                    for link in html.find_all("a"):
                        URL = link.get("href").strip()
                        try:
                            # test links
                            status_code = getRequestStatus(URL)
                            if (
                                (allIncluded == 0 or allIncluded == 2)
                                and status_code == 404
                                or status_code == 401
                            ):
                                if CLICOLOR:
                                    print(redColor + "Bad link " + URL + noColor)
                                else:
                                    print("Bad link " + URL)
                            elif (
                                allIncluded == 1 or allIncluded == 0
                            ) and status_code == 200:
                                if CLICOLOR:
                                    print(greenColor + "Good link " + URL + noColor)
                                else:
                                    print("Good link " + URL)
                            else:
                                if allIncluded == 0:
                                    if CLICOLOR:
                                        print(dgrayColor + "Unknown " + URL + noColor)
                                    else:
                                        print("Unknown " + URL)
                        except Exception:
                            if allIncluded == 0:
                                if CLICOLOR:
                                    print(dgrayColor + "Unknown " + URL + noColor)
                                else:
                                    print("Unknown " + URL)
                except Exception:
                    print(dgrayColor + "Unable to open file " + arg)


def goodBad(flag):
    if flag == "--good":
        return 1
    elif flag == "--bad":
        return 2
    else:
        return 0


def getRequestStatus(URL):
    requestObj = requests.get(URL, timeout=2)
    return requestObj.status_code

def fileValidation(fileName):
    if fileName[0] != "-" and fileName.find(".html") >= 0:
        return 0
    else:
        return -1

if __name__ == '__main__':
    main()