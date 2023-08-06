from .Common import Common as Parent
import json


class Group(Parent):

    def getAll(self):
        try:
            jsonResponse = self.requestUrl('/groups')
        except Exception as ex:
            print('Exception:', ex)
            return '%s' % ex

        if (jsonResponse['succes']):
            print('getAll', jsonResponse)
            return json.loads(jsonResponse['data'])
        else:
            return jsonResponse['messages'][0]

    def getNodes(self, name):
        return True