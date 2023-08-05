from .BaseAPI import BaseAPI
from .fb import Fb


class API:
    fb = None

    def __init__(self, token):
        self.api = BaseAPI(token)
        self.fb = Fb(self.api)

    @staticmethod
    def init(token):
        API.fb = Fb(BaseAPI(token))
