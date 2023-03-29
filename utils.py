def urljoin(*args):
    return "/".join(map(lambda x: str(x).rstrip('/').lstrip('/'), args)) + '/'

# def simpleDictToObject(dict, Class):
#     