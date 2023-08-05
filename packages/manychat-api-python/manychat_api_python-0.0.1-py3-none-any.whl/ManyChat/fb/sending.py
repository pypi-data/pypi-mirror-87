from ..APIStructure import APIStructure
from ..BaseAPI import BaseAPI


class Sending(APIStructure):
    def __init__(self, api, parent=None):
        super().__init__('sending', api, parent)

    def sendContent(self, subscriber_id, data, message_tag=None, otn_topic_name=None):
        parameters = {
            'subscriber_id': subscriber_id,
            'data': data,
        }
        if message_tag is not None:
            parameters['message_tag'] = message_tag
        if otn_topic_name is not None:
            parameters['otn_topic_name'] = otn_topic_name
        return APIStructure('sendContent', self.api, self)(req_type=BaseAPI.POST, **parameters)

    def sendContentByUserRef(self, user_ref, data):
        return APIStructure('sendContentByUserRef', self.api, self)(req_type=BaseAPI.POST, user_ref=user_ref, data=data)

    def sendFlow(self, subscriber_id, flow_ns):
        return APIStructure('sendFlow', self.api, self)(req_type=BaseAPI.POST, subscriber_id=subscriber_id,
                                                        flow_ns=flow_ns)
