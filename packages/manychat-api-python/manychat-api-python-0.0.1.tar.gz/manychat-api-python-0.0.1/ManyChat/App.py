from .BaseAPI import BaseAppAPI


class App:
    def __init__(self, token, version=1):
        self.api = BaseAppAPI(token)
        self.version = version

    def trigger_event(self, subscriber_id, trigger_name, context=None):
        parameters = {
            'version': self.version,
            'subscriber_id': subscriber_id,
            'trigger_name': trigger_name,
            'context': context,
        }
        return self.api.post('/apps/wh', parameters)
