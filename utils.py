def urljoin(*args):
    return "/".join(map(lambda x: str(x).rstrip('/').lstrip('/'), args)) + ("/" if args[len(args) - 1].endswith("/") else "")

# def simpleDictToObject(dict, Class):
#     