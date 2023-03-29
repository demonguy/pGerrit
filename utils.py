from urllib.parse import quote

def urljoin(*args):
    return "/".join(map(lambda x: str(x).rstrip('/').lstrip('/'), args)) + ("/" if args[len(args) - 1].endswith("/") else "")

def urlformat(formattedString, *args):
    args = [quote(str(arg), safe="") for arg in args]
    return formattedString.format(*args)
        

# def simpleDictToObject(dict, Class):
#     