from .Common import Common as Parent


class ConnectionSet(Parent):
    def addconnection(self, connectionset, nodeA, configA, nodeB, configB):
        try:
            data = {
                'connectionSet' : connectionset,
                'nodeA' : nodeA,
                'configA' : configA,
                'nodeB': nodeB,
                'configB': configB
            }
            jsonResponse = self.requestUrl('/connectionsets', data, 'POST')
        except Exception as ex:
            if ('Error 30117' in str(ex)):
                return 'ERROR(3): One or more parameters were missing.\r'
            else:
                if Parent.VERBOSE:
                    print('Exception', ex)
                return '%s' % ex
        if Parent.VERBOSE:
            print('addconnection', jsonResponse)
        if (jsonResponse['succes']):
            return 'OK'
        else:
            if Parent.VERBOSE:
                print('Messages', jsonResponse['messages'][0])
            if (jsonResponse['messages'][0]['msgCode'] == 30117):
                return 'ERROR(3): One or more parameters were missing.'
            if (jsonResponse['messages'][0]['msgCode'] == 30030):
                return 'ERROR(30): The specified node is unknown.'
            if (jsonResponse['messages'][0]['msgCode'] == 30034):
                return 'ERROR(34): The specified configuration is unknown.'
            else:
                return jsonResponse['messages'][0]

        return ''

    def removeConnection(self, connectionSet):
        try:
            jsonResponse = self.requestUrl('/connectionsets/%s' % (connectionSet), '', 'DELETE')
        except Exception as ex:
            if ('Error 30117' in str(ex)):
                return 'ERROR(3): One or more parameters were missing.\r'
            else:
                if Parent.VERBOSE:
                    print('Exception', ex)
                return '%s' % ex
        if Parent.VERBOSE:
            print('addconnection', jsonResponse)
        if (jsonResponse['succes']):
            return 'OK'
        else:
            if Parent.VERBOSE:
                print('Messages', jsonResponse['messages'][0])
            if (jsonResponse['messages'][0]['msgCode'] == 30117):
                return 'ERROR(3): One or more parameters were missing.'
            else:
                return jsonResponse['messages'][0]
