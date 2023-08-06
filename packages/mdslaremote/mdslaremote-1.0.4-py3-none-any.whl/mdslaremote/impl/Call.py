from .Common import Common as Parent


class Call(Parent):
    def getcallssincetest(self, testid, callid):
        try:
            jsonResponse = self.requestUrl('/calls?testID=%s&callID=%s' % (testid, callid))
        except Exception as ex:
            if ('Error 30117' in str(ex)):
                return 'ERROR(3): One or more parameters were missing.\r'
            else:
                print('Exception', ex)
                return '%s' % ex

        print('getcallssincetest', jsonResponse)
        if (jsonResponse['succes']):
            list = jsonResponse['data']
            print('List', list)
            if (list == ''): list = 'OK'
            return list
        else:
            print('Messages', jsonResponse['messages'][0])
            if (jsonResponse['messages'][0].msgCode == 30117):
                return 'ERROR(3): One or more parameters were missing.'
            else:
                return jsonResponse['messages'][0]

        return ''

    def getnextcallstart(self, testID):
        try:
            jsonResponse = self.requestUrl('/calls/next?testID=%s' % testID)
        except Exception as ex:
            print('Exception', ex)
            return '%s' % ex

        if (jsonResponse['succes']):
            data = jsonResponse['data']
            return data
        else:
            print('Error', jsonResponse['messages'][0], jsonResponse['messages'][0]['msgCode'])
            if (jsonResponse['messages'][0]['msgCode'] == 30012):
                return 'ERROR(12): Negative identifiers are not allowed.'
            else:
                return jsonResponse['messages'][0]


    def getcallprogress(self, callID):
        try:
            jsonResponse = self.requestUrl('/calls/%s/progress' % callID)
        except Exception as ex:
            print('Exception', ex)
            return '%s' % ex

        if (jsonResponse['succes']):
            data = jsonResponse['data']
            return data
        else:
            return jsonResponse['messages'][0]
