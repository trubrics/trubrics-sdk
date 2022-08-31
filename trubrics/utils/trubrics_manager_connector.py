from urllib.request import Request, urlopen


def make_request(url, headers=None, data=None):
    request = Request(url, headers=headers or {}, data=data)
    with urlopen(request, timeout=20) as response:
        return response.read()
