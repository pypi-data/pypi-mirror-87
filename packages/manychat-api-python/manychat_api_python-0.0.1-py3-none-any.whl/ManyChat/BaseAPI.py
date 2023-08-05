import urllib.request
import urllib.parse
import json


class BaseAPI:
    BASE_URL = 'https://api.manychat.com/'

    GET = 1
    POST = 2

    def __init__(self, token):
        self.token = token
        self.base_headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json',
        }

    def get(self, path, parameters=None, headers=None):
        final_headers = dict(self.base_headers)
        if headers is not None:
            final_headers.update(headers)
        url = urllib.parse.urljoin(self.BASE_URL, path)
        if parameters:
            url += '?' + urllib.parse.urlencode(parameters)
        req = urllib.request.Request(url, headers=final_headers)
        response = urllib.request.urlopen(req)
        return json.loads(response.read())

    def post(self, path, parameters, headers=None):
        final_headers = dict(self.base_headers)
        if headers is not None:
            final_headers.update(headers)
        url = urllib.parse.urljoin(self.BASE_URL, path)
        req = urllib.request.Request(url, data=json.dumps(parameters).encode('utf-8'), headers=final_headers)
        response = urllib.request.urlopen(req)
        return json.loads(response.read())

    def call_method(self, method, parameters=None, req_type=None):
        if req_type is None:
            req_type = BaseAPI.GET
        if req_type == BaseAPI.GET:
            result = self.get(method, parameters)
        elif req_type == BaseAPI.POST:
            result = self.post(method, parameters)
        else:
            raise
        return result


class BaseAppAPI(BaseAPI):
    BASE_URL = 'https://manychat.com'
