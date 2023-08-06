import requests

def slice(endpoint, guid, dim, lineno, headers = None):
    return f'{endpoint}/query/slice/{dim}/{lineno}'
