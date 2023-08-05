from ..APIStructure import APIStructure
from ..BaseAPI import BaseAPI


class Subscriber(APIStructure):
    def __init__(self, api, parent=None):
        super().__init__('subscriber', api, parent)

    def getInfo(self, subscriber_id):
        return APIStructure('getInfo', self.api, self)(subscriber_id=subscriber_id)

    def findByName(self, name):
        return APIStructure('findByName', self.api, self)(name=name)

    def getInfoByUserRef(self, user_ref):
        return APIStructure('getInfoByUserRef', self.api, self)(user_ref=user_ref)

    def findByCustomField(self, field_id, field_value):
        return APIStructure('findByCustomField', self.api, self)(field_id=field_id, field_value=field_value)

    def findBySystemField(self, email=None, phone=None):
        parameters = {}
        if email is not None:
            parameters['email'] = email
        if phone is not None:
            parameters['phone'] = phone
        return APIStructure('findBySystemField', self.api, self)(**parameters)

    def addTag(self, subscriber_id, tag_id):
        return APIStructure('addTag', self.api, self)(req_type=BaseAPI.POST, subscriber_id=subscriber_id, tag_id=tag_id)

    def addTagByName(self, subscriber_id, tag_name):
        return APIStructure('addTagByName', self.api, self)(req_type=BaseAPI.POST, subscriber_id=subscriber_id,
                                                            tag_name=tag_name)

    def removeTag(self, subscriber_id, tag_id):
        return APIStructure('removeTag', self.api, self)(req_type=BaseAPI.POST, subscriber_id=subscriber_id, tag_id=tag_id)

    def removeTagByName(self, subscriber_id, tag_name):
        return APIStructure('removeTagByName', self.api, self)(req_type=BaseAPI.POST, subscriber_id=subscriber_id,
                                                               tag_name=tag_name)

    def setCustomField(self, subscriber_id, field_id, field_value):
        return APIStructure('setCustomField', self.api, self)(req_type=BaseAPI.POST, subscriber_id=subscriber_id,
                                                              field_id=field_id, field_value=field_value)

    def setCustomFields(self, subscriber_id, fields):
        return APIStructure('setCustomFields', self.api, self)(req_type=BaseAPI.POST, subscriber_id=subscriber_id,
                                                               fields=fields)

    def setCustomFieldByName(self, subscriber_id, field_name, field_value):
        return APIStructure('setCustomFieldByName', self.api, self)(req_type=BaseAPI.POST, subscriber_id=subscriber_id,
                                                                    field_name=field_name, field_value=field_value)

    def verifyBySignedRequest(self, subscriber_id, signed_request):
        return APIStructure('verifyBySignedRequest', self.api, self)(req_type=BaseAPI.POST, subscriber_id=subscriber_id,
                                                                     signed_request=signed_request)

    def createSubscriber(self, first_name=None, last_name=None, phone=None, email=None,
                         gender=None, has_opt_in_sms=None, has_opt_in_email=None, consent_phrase=None):
        parameters = {}
        if first_name is not None:
            parameters['first_name'] = first_name
        if last_name is not None:
            parameters['last_name'] = last_name
        if email is not None:
            parameters['email'] = email
        if phone is not None:
            parameters['phone'] = phone
        if gender is not None:
            parameters['gender'] = gender
        if has_opt_in_sms is not None:
            parameters['has_opt_in_sms'] = has_opt_in_sms
        if has_opt_in_email is not None:
            parameters['has_opt_in_email'] = has_opt_in_email
        if consent_phrase is not None:
            parameters['consent_phrase'] = consent_phrase
        return APIStructure('createSubscriber', self.api, self)(req_type=BaseAPI.POST, **parameters)

    def updateSubscriber(self, subscriber_id, first_name=None, last_name=None, phone=None, email=None,
                         gender=None, has_opt_in_sms=None, has_opt_in_email=None, consent_phrase=None):
        parameters = {
            'subscriber_id': subscriber_id,
        }
        if first_name is not None:
            parameters['first_name'] = first_name
        if last_name is not None:
            parameters['last_name'] = last_name
        if email is not None:
            parameters['email'] = email
        if phone is not None:
            parameters['phone'] = phone
        if gender is not None:
            parameters['gender'] = gender
        if has_opt_in_sms is not None:
            parameters['has_opt_in_sms'] = has_opt_in_sms
        if has_opt_in_email is not None:
            parameters['has_opt_in_email'] = has_opt_in_email
        if consent_phrase is not None:
            parameters['consent_phrase'] = consent_phrase
        return APIStructure('updateSubscriber', self.api, self)(req_type=BaseAPI.POST, **parameters)
