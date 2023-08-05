import argparse
import requests
import threading
import sys
import re

from colorama import Fore, init

init()


def checkGoodLinks(links):
    for link in links:
        try:
            r = requests.head(link, timeout=10)  # gets status code
            if 200 <= r.status_code <= 299:
                print(f"{Fore.GREEN} {str(link)} {str(r)} Good! {Fore.RESET}")
        except requests.exceptions.RequestException:
            continue
        except requests.exceptions.Timeout:
            continue


def checkBadLinks(links):
    for link in links:
        try:
            r = requests.head(link, timeout=10)  # gets status code
            if 200 < r.status_code > 299:
                if 200 < r.status_code > 299 and 400 <= r.status_code <= 599:
                    print(f"{Fore.RED} {str(link)} {str(r)} Bad! {Fore.RESET}")
        except requests.exceptions.RequestException:
            print(f"{Fore.RED} Error: could not connect to {str(link)}!")
        except requests.exceptions.Timeout:
            print(f"{Fore.RED} Error: connection to {str(link)} timed out!")
        finally:
            continue


def checkUnignoredLinks(links, ignore):
    try:
        with open(ignore, "r") as f:
            line = f.read()
            if line[0] == "#":
                comment = True
            ignoredUrls = re.findall(r'https?://[^\s<>"].[^\s<>"]+', line)
        if len(ignoredUrls) == 0 and comment is False:
            raise FileNotFoundError
        urls = [
            x for x in links if x not in ignoredUrls
        ]  # remove ignored urls then check result
        return urls
    except FileNotFoundError:
        print(f"{Fore.RED}Error: invalid text file.")
        sys.exit(2)


def checkSingleLink(link):
    r = requests.head(link)
    return r


def checkLinks(links):
    exitCode = 0
    for link in links:
        try:
            r = requests.head(link, timeout=10)  # gets status code
            if 200 <= r.status_code <= 299:
                print(f"{Fore.GREEN} {str(link)} {str(r)} Good! {Fore.RESET}")
            elif 400 <= r.status_code <= 599:
                print(f"{Fore.RED} {str(link)} {str(r)} Bad!{Fore.RESET}")
                exitCode = 1
            else:
                print(f"{str(link)} {str(r)} Unknown!")
        except requests.exceptions.RequestException:
            print(f"{Fore.RED} Error: could not connect to website!")
            exitCode = 1
            continue
        except requests.exceptions.Timeout:
            print(f"{Fore.RED} Error: connection to website timed out!")
            exitCode = 1
            continue

    sys.exit(exitCode)


def checkTelescopePosts():
    links = []
    posts = requests.get("http://localhost:3000/posts")
    for post in posts.json():
        links.append("http://localhost:3000" + post["url"])
    if len(links) == 0:
        print(f"{Fore.RED} Error: no links found!")
    else:
        checkLinks(links)


def loadFile(filename):
    try:
        with open(filename, "r") as f:
            links = re.findall(
                r'https?://[^\s<>"].[^\s<>"]+', f.read()
            )  # find all urls and add them to array
        return links
    except FileNotFoundError:
        print(f"{Fore.RED} Error: the file could not be opened.")
        sys.exit(2)


def main():
    index = 2
    if len(sys.argv) > 1:
        if sys.argv[1] == "-t" or sys.argv[1] == "--telescope":
            checkTelescopePosts()
        else:
            links = loadFile(sys.argv[index])
            if len(links) == 0:
                print(f"{Fore.RED} Error: no links found!")
            else:
                if sys.argv[1] == "-g" or sys.argv[1] == "--good":
                    checkGoodLinks(links)
                elif sys.argv[1] == "-b" or sys.argv[1] == "--bad":
                    checkBadLinks(links)
                elif sys.argv[1] == "-i" or sys.argv[1] == "--ignore":
                    ignore = sys.argv[3]
                    result = checkUnignoredLinks(links, ignore)
                    checkLinks(result)
                else:
                    checkLinks(links)


def parseArgs():
    # Create parser that allows for arguments to be used with the tool
    parser = argparse.ArgumentParser(description="Checks for dead urls in a file")
    parser.add_argument(
        "-a", "--all", help="Checks urls in text file (e.g, main.py -c index.html)"
    )
    parser.add_argument("-g", "--good", help="Displays all good links in file")
    parser.add_argument("-b", "--bad", help="Displays all bad links in file")
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version="deadlinkz v0.1",
        help="Displays version info",
    )
    parser.add_argument("-i", "--ignore", nargs="+", help="Ignore links")
    parser.add_argument(
        "-t",
        "--telescope",
        action="store_true",
        help="Checks Telescope links obtained from the API",
    )
    return parser.parse_args()


args = parseArgs()
threading.Thread(target=main()).start()
