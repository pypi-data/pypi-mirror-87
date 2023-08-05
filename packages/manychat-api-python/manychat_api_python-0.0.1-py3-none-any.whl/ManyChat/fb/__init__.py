from ..APIStructure import APIStructure
from .page import Page
from .sending import Sending
from .subscriber import Subscriber


class Fb(APIStructure):
    def __init__(self, api):
        super().__init__('fb', api)
        self.page = Page(api, self)
        self.sending = Sending(api, self)
        self.subscriber = Subscriber(api, self)
