from urllib.request import Request, urlopen


def make_request(url, headers=None, data=None, method="GET"):
    request = Request(url, headers=headers or {}, data=data, method=method)
    with urlopen(request, timeout=20) as response:
        return response.read()
