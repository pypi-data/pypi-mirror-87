import requests
import re
import argparse
from colorama import init, Fore, Style

init()  # Colour support for Windows operating systems

parser = argparse.ArgumentParser(
    description="link-check is a broken link identifier"
)
parser.add_argument(
    "-v",
    "--version",
    action="store_true",
    help="Returns the current version of tool",
)
parser.add_argument(
    "-f",
    "--file",
    help="Checks the given file in the current directory for urls (-f htmls.txt)",
    metavar="\b",
)
parser.add_argument(
    "-r",
    "--redirect",
    help="Checks the given file in the current directory for urls and allows for redirecting of urls (-r htmls.txt)",
    metavar="\b",
)
parser.add_argument(
    "-j",
    "--json",
    help="Prints all urls in a json object on the command line",
    nargs="*",
    metavar="",
)
parser.add_argument(
    "-g",
    "--good",
    help="Prints only good urls (status = 200-299)",
    nargs="*",
    metavar="",
)
parser.add_argument(
    "-b",
    "--bad",
    help="Prints only bad urls (status = 400-499)",
    nargs="*",
    metavar="",
)
parser.add_argument(
    "-i",
    "--ignore",
    help="Supply a text file with urls to ignore checking in the given file",
    metavar="",
)
parser.add_argument(
    "-t",
    "--telescope",
    help="Runs link-check on the 10 most recent telescope posts",
    nargs="*",
    metavar="",
)
parser.add_argument(
    "-u",
    "--url",
    help="Runs a single url written on the command line through link_check",
    nargs="*",
    metavar="",
)

args = parser.parse_args()


# Prints the corresponding message for the status code
def checkUrl(status_code, url):
    if args.json is not None:
        jsonObj = {"url": url, "status": status_code}
        if args.good is not None:
            if status_code in range(200, 299):
                jsonArr.append(jsonObj)
        elif args.bad is not None:
            if status_code in range(400, 599):
                jsonArr.append(jsonObj)
        else:
            jsonArr.append(jsonObj)
    elif args.good is not None:
        if status_code in range(200, 299):
            print(Fore.GREEN, url[0], status_code, " GOOD", Style.RESET_ALL)
    elif args.bad is not None:
        if status_code in range(400, 599):
            print(
                Fore.RED,
                url[0],
                status_code,
                " CLIENT/SERVER ISSUE",
                Style.RESET_ALL,
            )
    else:
        if status_code in range(200, 299):
            print(Fore.GREEN, url[0], status_code, " GOOD", Style.RESET_ALL)
            output = "GOOD"
        elif status_code in range(300, 399):
            print(
                Fore.YELLOW, url[0], status_code, " REDIRECT", Style.RESET_ALL
            )
            output = "REDIRECT"
        elif status_code in range(400, 599):
            print(
                Fore.RED,
                url[0],
                status_code,
                " CLIENT/SERVER ISSUE",
                Style.RESET_ALL,
            )
            output = "CLIENT/SERVER ISSUE"
        else:
            print(Fore.WHITE, url[0], status_code, " UNKNOWN", Style.RESET_ALL)
            output = "UNKNOWN"
    return output


# Returns the status code of the given URLs
def requestUrl(urls):
    try:
        if args.file:
            r = requests.head(urls[0], timeout=1.5)
        elif args.redirect:
            r = requests.head(urls[0], timeout=1.5, allow_redirects=True)
        else:
            r = requests.head(urls[0], timeout=1.5)
        return r.status_code
    except requests.exceptions.RequestException:
        print(" ", Fore.RED + urls[0], "TIMEOUT", Style.RESET_ALL)
        output = "TIMEOUT"
        return output


# Parses the URL from the given file
def urlParse():  # pragma: no cover
    foundUrls = []
    if args.file:
        argFile = args.file
    elif args.redirect:
        argFile = args.redirect
    try:
        with open(argFile) or open(argFile) as file:
            for line in file:
                urls = re.findall(
                    r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",
                    line,
                )
                if len(urls) != 0:
                    if args.ignore:
                        if not ignoreURL(urls):
                            foundUrls.append(urls)
                    else:
                        foundUrls.append(urls)
    except Exception as e:
        print(f"\n{e}")
    return foundUrls


def singleUrlCheck(status_code, url):
    if status_code in range(200, 299):
        print(Fore.GREEN, url, status_code, " GOOD", Style.RESET_ALL)
        output = "GOOD"
    elif status_code in range(300, 399):
        print(Fore.YELLOW, url, status_code, " REDIRECT", Style.RESET_ALL)
        output = "REDIRECT"
    elif status_code in range(400, 599):
        print(
            Fore.RED,
            url,
            status_code,
            " CLIENT/SERVER ISSUE",
            Style.RESET_ALL,
        )
        output = "CLIENT/SERVER ISSUE"
    else:
        print(Fore.WHITE, url, status_code, " UNKNOWN", Style.RESET_ALL)
        output = "UNKNOWN"
    return output


# Returns true if url is in the ignore list.
def ignoreURL(url):  # pragma: no cover
    ignore = False
    ignoreFile = args.ignore
    try:
        with open(ignoreFile) or open(ignoreFile) as file:
            toIgnore = re.findall(r"^http[s]?://.*[^\s/]", file.read(), re.M)
            file.seek(0)
            for line in file:
                if re.match("#", line) or re.match("\n", line):
                    pass
                elif re.match(r"^http[s]?://", line):
                    for domain in toIgnore:
                        if re.match(f"{domain}", url[0]):
                            ignore = True
                else:
                    raise ValueError(
                        '\nInvalid file format for --ignore. Lines must start with "#", "http://", or "https://" only.'
                    )
    except FileNotFoundError:
        raise
    return ignore


if args.version:  # pragma: no cover
    version = 0.5
    print(
        Fore.GREEN + "Link" + Fore.RED + " Check",
        Style.RESET_ALL,
        "v.",
        version,
    )
elif args.file or args.redirect:  # pragma: no cover
    if args.json is not None:
        jsonArr = []
        print(
            Fore.YELLOW,
            " ** JSON Object creation is slow ** \n",
            Fore.GREEN,
            "** JSON Object being created... **",
            Style.RESET_ALL,
        )
        foundUrls = urlParse()
        for url in foundUrls:
            status_code = requestUrl(url)
            checkUrl(status_code, url)
        print(jsonArr)
    else:
        foundUrls = urlParse()
        for url in foundUrls:
            status_code = requestUrl(url)
            checkUrl(status_code, url)
elif args.telescope is not None:  # pragma: no cover
    r = requests.get("http://localhost:3000/posts", timeout=1.5)
    if r.status_code != 200:
        print("Local telescope server does not respond with 200")
    else:
        jsonResponse = r.json()
        for post in jsonResponse:
            postRequest = requests.get("http://localhost:3000" + post["url"])
            urls = re.findall(
                r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",
                str(postRequest.json()),
            )
            urls = list(dict.fromkeys(urls))
            for url in urls:
                if url[-1] == ",":
                    url = url[:-2]
                try:
                    r = requests.get(url, timeout=1.5, allow_redirects=True)
                    checkUrl(r.status_code, url)
                except requests.exceptions.RequestException:
                    print(Fore.RED + url, "TIMEOUT")
elif args.url is not None:  # pragma: no cover
    status_code = requestUrl(args.url)
    singleUrlCheck(status_code, args.url)
