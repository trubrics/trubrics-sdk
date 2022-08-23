from urllib.request import Request, urlopen

import google.auth.transport.requests
import google.oauth2.id_token


def get_gcp_id_token(url):
    auth_req = google.auth.transport.requests.Request()
    id_token = google.oauth2.id_token.fetch_id_token(auth_req, url)
    return id_token


def make_request(url, headers=None, data=None):
    request = Request(url, headers=headers or {}, data=data)
    with urlopen(request, timeout=10) as response:
        print(response.status)
        return response.read()
