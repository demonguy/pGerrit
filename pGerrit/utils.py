from urllib.parse import quote
import re

def urljoin(*args):
    return "/".join(map(lambda x: str(x).rstrip('/').lstrip('/'), args)) + ("/" if args[len(args) - 1].endswith("/") else "")

def urlformat(formattedString, *args):
    args = [quote(str(arg), safe="") for arg in args]
    return formattedString.format(*args)

def parseCookieFile(cookiefile):
    """Parse a cookies.txt file and return a dictionary of key value pairs
    compatible with requests."""

    cookies = {}
    with open (cookiefile, 'r') as fp:
        for line in fp:
            if not re.match(r'^\#', line):
                lineFields = line.strip().split('\t')
                cookies[lineFields[5]] = lineFields[6]
    return cookies
        

# def simpleDictToObject(dict, Class):
#     