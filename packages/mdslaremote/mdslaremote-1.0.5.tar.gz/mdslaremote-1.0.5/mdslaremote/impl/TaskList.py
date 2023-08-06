from .Common import Common as Parent
import base64

class TaskList(Parent):
    def upload(self, fileName, data):
        strByte = data.encode('utf-8')
        if Parent.VERBOSE:
            print('strByte', strByte)

        strBase64 = base64.encodebytes(strByte)
        if Parent.VERBOSE:
            print('strBase64', strBase64)

        dataJson = {
            'filepath': fileName,
            'data': strBase64,
            'overwrite': False
        }
        try:
            jsonResponse = self.requestUrl('/tasklist', dataJson, 'POST')
        except Exception as ex:
            if Parent.VERBOSE:
                print('Exception', ex)
            return '%s' % ex
        if Parent.VERBOSE:
            print('Stop', jsonResponse)
        if (jsonResponse['succes']):
                return 'OK'
        else:
            if (jsonResponse['messages'][0]['msgCode'] == 30350):
                return 'ERROR(3): One or more parameters were missing.'
            elif (jsonResponse['messages'][0]['msgCode'] == 30071):
                return 'ERROR(71): The file already exists.'
            else:
                return jsonResponse['messages'][0]['msgBasicContentText']