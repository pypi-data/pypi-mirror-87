from .Common import Common as Parent
import urllib
import io
import json
import base64


class Node(Parent):
    def getAll(self):
        url = self.getUrl('/nodes')
        f = urllib.request.urlopen(url)
        reads = f.read()
        print('Read:', reads)

        jsonResponse = json.loads(reads.decode("utf-8"))
        if (not 'succes' in jsonResponse):
            return False

        return json.loads(jsonResponse['data'])
        # response = requests.get(self.getUrl('/nodes'))
        # nodes = response.json()
        # return json.loads(nodes['data'])
        # return 'data'

    def add(self, name, type, address, hasPolqa, groupName, quantity=1, configsName=None):
        data = {
            'BaseName': name,
            'NodeTypeName': type,
            'Address': address,
            'POLQA': hasPolqa,
            'GroupName': groupName,
            'Quantity': quantity,
            'ConfigsNameNode': configsName
        }
        try:
            jsonResponse = self.requestUrl('/nodes', data, 'POST')
        except Exception as ex:
            return '%s' % ex

        if (jsonResponse['succes']):
            nodesName = ''
            nodesID = jsonResponse['data']
            for node in nodesID.split(';'):
                try:
                    jsonResponse = self.requestUrl('/nodes/%s' % node)
                except Exception as ex:
                    return '%s' % ex

                if (jsonResponse['succes']):
                    nodeData = json.loads(jsonResponse['data'])
                    if (nodesName == ''):
                        nodesName = nodeData['name']
                    else:
                        nodesName = '%s;%s' % (nodesName, nodeData['name'])

            return nodesName
        elif (jsonResponse['messages'][0]['msgCode'] == 30052):
            return "ERROR(52): The specified node type is unknown."
        else:
            return jsonResponse['messages'][0]

    def get(self, name):
        try:
            jsonResponse = self.requestUrl('/nodes')
        except Exception as ex:
            return '%s' % ex

        if (jsonResponse['succes']):
            nodes = json.loads(jsonResponse['data'])
            for node in nodes:
                if (node['name'] == name):
                    return node

        return 'ERROR(30): The specified node is unknown.'

    def delete(self, name):
        node = self.get(name)
        if 'ERROR' in node:
            return node

        try:
            jsonResponse = self.requestUrl('/nodes/%d' % node['id'], method='DELETE')
        except Exception as ex:
            return '%s' % ex

        if (jsonResponse['succes']):
            return 'OK'
        else:
            return jsonResponse['messages'][0]

    def copy(self, nameSource, nameDestination, address):
        data = {
            'destinationName': nameDestination,
            'destinationIP': address,
        }

        node = self.get(nameSource)
        if node == None:
            print('Not Found')
            return False
        if Parent.VERBOSE:
            print('Copy', node)
        try:
            jsonResponse = self.requestUrl('/nodes/%d/clone' % node['id'], data, 'POST')
        except Exception as ex:
            return '%s' % ex

        if (jsonResponse['succes']):
            return 'OK'
        else:
            return jsonResponse['messages'][0]

    def getTypes(self):
        try:
            jsonResponse = self.requestUrl('/nodes/types')
        except Exception as ex:
            if Parent.VERBOSE:
                print('Exception:', ex)
            return '%s' % ex

        if (jsonResponse['succes']):
            returnValues = None
            types = json.loads(jsonResponse['data'])
            for type in types:
                if (returnValues == None):
                    returnValues = type
                else:
                    returnValues = "%s;%s" % (returnValues, type)
            return returnValues
        else:
            return jsonResponse['messages'][0]

    def importFile(self, filePath):
        # xmlfile
        try:
            fileRead = io.open(filePath, mode="r", encoding="utf-16")
            xmlData = fileRead.read()
            fileRead.close()
            if Parent.VERBOSE:
                print('Str:', xmlData)

            strByte = xmlData.encode('utf-8')
            if Parent.VERBOSE:
                print('strByte', strByte)

            strBase64 = base64.encodebytes(strByte)
            if Parent.VERBOSE:
                print('strBase64', strBase64)

            # strURLEncode = urllib.parse.quote(strBase64)
            # print('strURLEncode', strURLEncode)

            data = {
                'xmlfile': strBase64
            }
            if Parent.VERBOSE:
                print('File:', data)
        except Exception as fileEx:
            if Parent.VERBOSE:
                print('importFile exception', fileEx)
            return 'ERROR(55): The node restore operation failed.'

        try:
            jsonResponse = self.requestUrl('/nodes/restore', data, 'POST')
        except Exception as ex:
            if Parent.VERBOSE:
                print('Exception:', ex)
            return '%s' % ex

        if (jsonResponse['succes']):
            return 'OK'
        else:
            return jsonResponse['messages'][0]

    def getStatus(self, name):
        node = self.get(name)
        if 'ERROR' in node:
            return node

        try:
            jsonResponse = self.requestUrl('/nodes/%d/checkstatus?blocking=True' % node['id'], method='GET')
        except Exception as ex:
            return '%s' % ex

        if (jsonResponse['succes']):
            if (jsonResponse['data'] == '0'):
                return 'ERROR(32): The status of the node is unknown.'
            elif (jsonResponse['data'] == '1'):
                return 'ERROR(33): The node is unreachable.'
            elif (jsonResponse['data'] == '2'):
                return 'OK'
            elif (jsonResponse['data'] == '5'):
                return 'The node is currently connected.'
        else:
            return jsonResponse['messages'][0]

    def isRunningTest(self, name):
        node = self.get(name)
        if 'ERROR' in node:
            return node

        try:
            jsonResponse = self.requestUrl('/tests/progressnode?nodeid=%d' % node['id'], method='GET')
        except Exception as ex:
            return '%s' % ex
        if Parent.VERBOSE:
            print('Data:', jsonResponse)
        if (jsonResponse['succes']):
            progress = json.loads(jsonResponse['data'])
            if Parent.VERBOSE:
                print('Progress:', progress)
            if progress['running']:
                return 'TRUE'
            else:
                return 'FALSE'
        else:
            return jsonResponse['messages'][0]

    def getVersion(self, name):
        node = self.get(name)
        if 'ERROR' in node:
            return node

        try:
            jsonResponse = self.requestUrl('/nodes/%d/getVersion' % node['id'], method='GET')
        except Exception as ex:
            return '%s' % ex
        if Parent.VERBOSE:
            print('Data:', jsonResponse)
        if (jsonResponse['succes']):
            return jsonResponse['data']
        else:
            return jsonResponse['messages'][0]

    def reset(self, name):
        node = self.get(name)
        if 'ERROR' in node:
            return node

        try:
            jsonResponse = self.requestUrl('/nodes/%d/reset' % node['id'], method='GET')
        except Exception as ex:
            return '%s' % ex
        if Parent.VERBOSE:
            print('Data:', jsonResponse)
        if (jsonResponse['succes']):
            return 'OK'
        else:
            return jsonResponse['messages'][0]

    def getfsclrtimeout(self):
        try:
            jsonResponse = self.requestUrl('/nodes/formattimeout')
        except Exception as ex:
            if Parent.VERBOSE:
                print('Exception:', ex)
            return '%s' % ex

        if (jsonResponse['succes']):
            return 'NODE GETFSCLRTIMEOUT: timeout=%s' % jsonResponse['data']
        else:
            return jsonResponse['messages'][0]

    def setfsclrtimeout(self, timeout):
        data = {
            'value': timeout
        }
        try:
            jsonResponse = self.requestUrl('/nodes/formattimeout', data, 'PATCH')
        except Exception as ex:
            if Parent.VERBOSE:
                print('Exception:', ex)
            return '%s' % ex
        if Parent.VERBOSE:
            print('setfsclrtimeout', jsonResponse)
        if (jsonResponse['succes']):
            return 'OK; NODE SETFSCLRTIMEOUT: timeout=%s msec for this session.' % timeout
        elif jsonResponse['messages'][0]['msgCode'] == 30013:
            return 'ERROR(13): Negative numbers are not allowed.'
        else:
            return jsonResponse['messages'][0]

    def clearfilesystem(self, name):
        node = self.get(name)
        if 'ERROR(30):' in node:
            return 'ERROR(4): One or more parameters were of an invalid type or value.'
        elif 'ERROR' in node:
            return node

        try:
            jsonResponse = self.requestUrl('/nodes/%d/filesystem/format' % node['id'])
        except Exception as ex:
            if Parent.VERBOSE:
                print('Exception:', ex)
            return '%s' % ex
        if Parent.VERBOSE:
            print('Clear', jsonResponse)
        if (jsonResponse['succes']):
            index = jsonResponse['data'].index('available memory ')
            if (index > 0):
                return 'NODE CLEARFILESYSTEM: free memory=%s' % jsonResponse['data'][index + 17]
            else:
                return jsonResponse['data']
        elif jsonResponse['messages'][0]['msgCode'] == 30109:
            return 'ERROR(32): The status of the node is unknown.'
        else:
            return jsonResponse['messages'][0]

    def getConfigID(self, nodeID, name):
        try:
            jsonResponse = self.requestUrl('/nodes/%d/configs' % (nodeID))
        except Exception as ex:
            if Parent.VERBOSE:
                print('Exception:', ex)
            return '%s' % ex

        if (jsonResponse['succes']):
            nodes = json.loads(jsonResponse['data'])
            if Parent.VERBOSE:
                print('Json response', nodes)
            for node in nodes:
                if (node['ConfigName'] == name):
                    if Parent.VERBOSE:
                        print('get node', node['NodeName'])
                    return node['ConfigID']
            return 'ERROR(34): The specified configuration is unknown.'
        else:
            return jsonResponse['messages'][0]

    def setconfigparam(self, name, configName, ParamName, value):
        node = self.get(name)
        if 'ERROR(30):' in node:
            return 'ERROR(4): One or more parameters were of an invalid type or value.'
        elif 'ERROR' in node:
            return node
        if Parent.VERBOSE:
            print('Node ID', node)

        configID = self.getConfigID(node['id'], configName)
        if Parent.VERBOSE:
            print('config ID', configID, type(configID))
        if type(configID) == str:
            return configID

        data = {
            'value': value
        }
        try:
            jsonResponse = self.requestUrl('/nodes/%d/configs/%s/%s' % (node['id'], configID, ParamName), data, 'PATCH')
        except Exception as ex:
            if Parent.VERBOSE:
                print('Exception:', ex)
            return '%s' % ex
        if Parent.VERBOSE:
            print('setconfigparam', jsonResponse)
        if (jsonResponse['succes']):
            return jsonResponse['data']
        else:
            return jsonResponse['messages'][0]

    def getconfigparam(self, name, configName, ParamName):
        node = self.get(name)
        if 'ERROR(30):' in node:
            return 'ERROR(4): One or more parameters were of an invalid type or value.'
        elif 'ERROR' in node:
            return node

        config = self.getConfigID(node['id'], configName)
        if Parent.VERBOSE:
            print('config ID', config, type(config))
        if type(config) == str:
            return config

        try:
            jsonResponse = self.requestUrl('/nodes/%d/configs/%s/%s' % (node['id'], config, ParamName))
        except Exception as ex:
            if Parent.VERBOSE:
                print('Exception:', ex)
            return '%s' % ex
        if Parent.VERBOSE:
            print('getconfigparam', jsonResponse)
        if (jsonResponse['succes']):
            return jsonResponse['data']
        else:
            return jsonResponse['messages'][0]

    def deleteConfiguration(self, name, configurationName):
        return True

    def getConfigurations(self, name):
        return True

    def upgradefirmware(self, nodename, path):
        node = self.get(nodename)
        if Parent.VERBOSE:
            print('Get node:', node)
        if 'ERROR' in node:
            return node
        if Parent.VERBOSE:
            print('Node ID', node)

        try:
            fileRead = io.open(path, mode="rb")
            binData = fileRead.read()
            fileRead.close()
        except Exception as ex:
            if Parent.VERBOSE:
                print(Exception, ex.args)
            if ex.args[0] == 2:
                return 'ERROR(4): One or more parameters were of an invalid type or value.'
            else:
                return ex

        strBase64 = base64.encodebytes(binData)
        if Parent.VERBOSE:
            print('strBase64', strBase64)

        data = {
            'firmware': strBase64
        }
        try:
            jsonResponse = self.requestUrl('/nodes/%d/upgradefirmware' % (node['id']), data, 'POST')
        except Exception as ex:
            if Parent.VERBOSE:
                print('Exception', ex)
            return '%s' % ex

        if (jsonResponse['succes']):
            return 'OK'
        else:
            return jsonResponse['messages'][0]
