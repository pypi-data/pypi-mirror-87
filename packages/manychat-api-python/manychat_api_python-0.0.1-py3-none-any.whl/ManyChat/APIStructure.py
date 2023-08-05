from .api import BaseAPI


class APIStructure:
    def __init__(self, name, api, parent=None):
        self.name = name
        self.api = api
        self.parent = parent

    def __getattr__(self, item):
        return APIStructure(item, self.api, self)

    def __str__(self):
        if self.parent is None:
            return '/' + self.name
        return str(self.parent) + '/' + self.name

    def __call__(self, req_type=BaseAPI.GET, **parameters):
        return self.api.call_method(str(self), parameters, req_type)
