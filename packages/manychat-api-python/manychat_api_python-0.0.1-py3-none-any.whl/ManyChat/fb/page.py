from ..APIStructure import APIStructure
from ..BaseAPI import BaseAPI


class Page(APIStructure):
    def __init__(self, api, parent=None):
        super().__init__('page', api, parent)

    def getInfo(self):
        return APIStructure('getInfo', self.api, self)()

    def createTag(self, name):
        return APIStructure('createTag', self.api, self)(req_type=BaseAPI.POST, name=name)

    def getTags(self):
        return APIStructure('getTags', self.api, self)()

    def removeTag(self, tag_id):
        return APIStructure('removeTag', self.api, self)(req_type=BaseAPI.POST, tag_id=tag_id)

    def removeTagByName(self, tag_name):
        return APIStructure('removeTagByName', self.api, self)(req_type=BaseAPI.POST, tag_name=tag_name)

    def getWidgets(self):
        return APIStructure('getWidgets', self.api, self)()

    def createCustomField(self, caption, type, description=None):
        parameters = {
            'caption': caption,
            'type': type,
        }
        if description is not None:
            parameters['description'] = description
        return APIStructure('createCustomField', self.api, self)(req_type=BaseAPI.POST, **parameters)

    def getGrowthTools(self):
        return APIStructure('getGrowthTools', self.api, self)()

    def getFlows(self):
        return APIStructure('getFlows', self.api, self)()

    def getCustomFields(self):
        return APIStructure('getCustomFields', self.api, self)()

    def getOtnTopics(self):
        return APIStructure('getOtnTopics', self.api, self)()

    def getBotFields(self):
        return APIStructure('getBotFields', self.api, self)()

    def createBotField(self, name, type, description=None, value=None):
        parameters = {
            'name': name,
            'type': type,
        }
        if description is not None:
            parameters['description'] = description
        if value is not None:
            parameters['value'] = value
        return APIStructure('createBotField', self.api, self)(req_type=BaseAPI.POST, **parameters)

    def setBotField(self, field_id, field_value):
        return APIStructure('setBotField', self.api, self)(req_type=BaseAPI.POST, field_id=field_id,
                                                           field_value=field_value)

    def setBotFieldByName(self, field_name, field_value):
        return APIStructure('setBotFieldByName', self.api, self)(req_type=BaseAPI.POST, field_name=field_name,
                                                           field_value=field_value)
