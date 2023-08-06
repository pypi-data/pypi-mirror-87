from . Common import Common as Parent
import urllib
import json
import time
import io
from datetime import datetime

class Test(Parent):

    def convertError(self, jsonResponse):
        if (jsonResponse['messages'][0]['msgCode'] == 103):
            return 'ERROR(3): One or more parameters were missing.'
        elif (jsonResponse['messages'][0]['msgCode'] == 30012):
            return 'ERROR(12): Negative identifiers are not allowed.'
        elif (jsonResponse['messages'][0]['msgCode'] == 30013):
            return 'ERROR(13): Negative numbers are not allowed.'
        elif (jsonResponse['messages'][0]['msgCode'] == 30108):
            return 'ERROR(3): One or more parameters were missing.'
        elif (jsonResponse['messages'][0]['msgCode'] == 30030):
            return 'ERROR(30): The specified node is unknown.'
        elif (jsonResponse['messages'][0]['msgCode'] == 30038):
            return 'ERROR(38): The specified connection set is unknown.'
        else:
            return jsonResponse['messages'][0]['msgBasicContentText']

    def schedule(self, mtlName, *args):
        if (len(args) > 5):
            if (args[5] == Parent.NOW):
                starttime = time.time()
            else:
                try:
                    starttime = time.mktime(time.strptime(args[5], '%d-%b-%Y %H:%M:%S'))
                except Exception as ex:
                    print('Bad date convertion', ex)
                    return 'ERROR(4): One or more parameters were of an invalid type or value.'
            timestamp = int(starttime)
            print('Timestamp', timestamp, starttime)
            data = {
                'name': mtlName,
                'nodeA': args[0],
                'nodeB': args[1],
                'executes': args[2],
                'calls': args[3],
                'period': args[4],
                'starttime': timestamp,
                'testIdToEdit': 0,
                'testName': ''
            }
            print('args 6', args)
        else:
            starttime = args[4]
            if (starttime == Parent.NOW):
                starttime = time.time()
            timestamp = int(starttime)
            print('Timestamp', timestamp, starttime)
            data = {
                    'name': mtlName,
                    'connectionSet': args[0],
                    'executes': args[1],
                    'calls': args[2],
                    'period': args[3],
                    'starttime': timestamp,
                    'testIdToEdit': 0,
                    'testName': ''
            }
            print('args 5', args)

        print('Data', data)
        try:
            jsonResponse = self.requestUrl('/tests/schedule', data, 'POST')
        except Exception as ex:
            print('Exception', ex)
            return '%s' % ex

        print('response', jsonResponse, jsonResponse['succes'])
        if (jsonResponse['succes']):
            data = jsonResponse['data']
            print('response data:', data)
            return data
        else:
            if (jsonResponse['messages'][0]['msgCode'] == 103):
                return 'ERROR(3): One or more parameters were missing.'
            elif (jsonResponse['messages'][0]['msgCode'] == 30012):
                return 'ERROR(12): Negative identifiers are not allowed.'
            elif (jsonResponse['messages'][0]['msgCode'] == 30013):
                return 'ERROR(13): Negative numbers are not allowed.'
            elif (jsonResponse['messages'][0]['msgCode'] == 30108):
                return 'ERROR(3): One or more parameters were missing.'
            elif (jsonResponse['messages'][0]['msgCode'] == 30030):
                return 'ERROR(30): The specified node is unknown.'
            else:
                return jsonResponse['messages'][0]['msgBasicContentText']

        return '0'

    def start(self, mtlName, *args):
        print('Start test', len(args))
        if (len(args) == 2):
            data = {
                'name': mtlName,
                'nodeA': args[0],
                'nodeB': args[1],
            }
        elif (len(args) == 1):
            data = {
                'name': mtlName,
                'connectionSet': args[0]
            }
        else:
            return 'KO'

        print('Data', data)
        try:
            jsonResponse = self.requestUrl('/tests/start', data, 'POST')
        except Exception as ex:
            print('Exception', ex)
            return '%s' % ex

        print('response', jsonResponse, jsonResponse['succes'])
        if (jsonResponse['succes']):
            data = jsonResponse['data']
            print('response data:', data)
            return data
        else:
            return self.convertError(jsonResponse)

        return '0'

    def stop(self, testID):
        try:
            jsonResponse = self.requestUrl('/tests/%s/stop' % (testID))
        except Exception as ex:
            print('Exception', ex)
            return '%s' % ex

        print('Stop', jsonResponse)
        if (jsonResponse['succes']):
                return 'OK'
        else:
            return self.convertError(jsonResponse)

    def terminateall(self):
        try:
            jsonResponse = self.requestUrl('/tests/terminateAll')
        except Exception as ex:
            print('Exception', ex)
            return '%s' % ex

        print('Stop', jsonResponse)
        if (jsonResponse['succes']):
            return 'OK'
        else:
            return self.convertError(jsonResponse)

    def getresultlist(self, testID, resulttype, eventnumber):
        try:
            jsonResponse = self.requestUrl('/tests/%s/results?resultType=%s' % (testID, resulttype))
        except Exception as ex:
            print('Exception', ex)
            return '%s' % ex

        if (jsonResponse['succes']):
            return self.convertResultJsonToXML(jsonResponse['data'])
        else:
            return jsonResponse['messages'][0]

        return '0'

    def getmeasuretypes(self):
        try:
            jsonResponse = self.requestUrl('/tests/measureTypes')
        except Exception as ex:
            print('Exception', ex)
            return '%s' % ex

        if (jsonResponse['succes']):
            data = jsonResponse['data']
            return data
        else:
            return jsonResponse['messages'][0]

    def getcurrenttestlist(self):
        ret = ''
        try:
            jsonResponse = self.requestUrl('/tests?onlycurrent=true')
        except Exception as ex:
            print('Exception', ex)
            return '%s' % ex

        if (jsonResponse['succes']):
            data = jsonResponse['data']
            y = json.loads(data)
            for test in y:
                dt_object = datetime.fromtimestamp(test['Agenda']['NextTestStartTS'])
                if (len(ret) > 0):
                    ret = '%s\r\n%s\t%s\t%s\t%s\t%s' % (ret, test['TestID'], test['Description'], dt_object.strftime('%Y-%m-%dT%H:%M:%S:%fZ'), test['NodeConfigPairs'][0]['Node'], test['NodeConfigPairs'][1]['Node'])
                else:
                    ret = '%s\t%s\t%s\t%s\t%s' % (test['TestID'], test['Description'], dt_object.strftime('%Y-%m-%dT%H:%M:%S:%fZ'), test['NodeConfigPairs'][0]['Node'], test['NodeConfigPairs'][1]['Node'])

            return ret
        else:
            return jsonResponse['messages'][0]

    def getfuturetestlist(self):
        ret = ''
        try:
            jsonResponse = self.requestUrl('/tests?onlyfuture=true')
        except Exception as ex:
            print('Exception', ex)
            return '%s' % ex

        print('getfuturetestlist', jsonResponse)
        if (jsonResponse['succes']):
            data = jsonResponse['data']
            y = json.loads(data)
            for test in y:
                dt_object = datetime.fromtimestamp(test['Agenda']['NextTestStartTS'])
                if (len(ret) > 0):
                    ret = '%s\r\n%s\t%s\t%s\t%s\t%s' % (
                    ret, test['TestID'], test['Description'], dt_object.strftime('%Y-%m-%dT%H:%M:%S:%fZ'),
                    test['NodeConfigPairs'][0]['Node'], test['NodeConfigPairs'][1]['Node'])
                else:
                    ret = '%s\t%s\t%s\t%s\t%s' % (
                    test['TestID'], test['Description'], dt_object.strftime('%Y-%m-%dT%H:%M:%S:%fZ'),
                    test['NodeConfigPairs'][0]['Node'], test['NodeConfigPairs'][1]['Node'])

            return ret
        else:
            return jsonResponse['messages'][0]

    def getrunningtestlist(self):
        ret = ''
        try:
            jsonResponse = self.requestUrl('/tests?onlyCurrent=true')
        except Exception as ex:
            print('Exception', ex)
            return '%s' % ex

        if (jsonResponse['succes']):
            data = jsonResponse['data']
            y = json.loads(data)
            for test in y:
                dt_object = datetime.fromtimestamp(test['Agenda']['NextTestStartTS'])
                if (len(ret) > 0):
                    ret = '%s\r\n%s\t%s\t%s\t%s\t%s' % (
                    ret, test['TestID'], test['Description'], dt_object.strftime('%Y-%m-%dT%H:%M:%S:%fZ'),
                    test['NodeConfigPairs'][0]['Node'], test['NodeConfigPairs'][1]['Node'])
                else:
                    ret = '%s\t%s\t%s\t%s\t%s' % (
                    test['TestID'], test['Description'], dt_object.strftime('%Y-%m-%dT%H:%M:%S:%fZ'),
                    test['NodeConfigPairs'][0]['Node'], test['NodeConfigPairs'][1]['Node'])

            return ret
        else:
            return jsonResponse['messages'][0]

    def gettestprogress(self, testID):
        ret = ''
        try:
            jsonResponse = self.requestUrl('/tests/%s/progress' % testID)
        except Exception as ex:
            print('Exception', ex)
            return '%s' % ex

        if (jsonResponse['succes']):
            data = jsonResponse['data']
            return data
        else:
            return jsonResponse['messages'][0]

    def getTaskListFile(self):
        ret = ''
        try:
            jsonResponse = self.requestUrl('/taskList/')
        except Exception as ex:
            print('Exception', ex)
            return '%s' % ex

        if (jsonResponse['succes']):
            data = jsonResponse['data']
            y = json.loads(data)
            for test in y:
                if (len(ret) > 0):
                    ret = '%s\r\n\%s' % (ret, test)
                else:
                    ret = '%s' % (test)

            return ret
        else:
            return jsonResponse['messages'][0]

    def terminatetest(self, testID):
        try:
            jsonResponse = self.requestUrl('/tests/%s/terminate' % testID)
        except Exception as ex:
            print('Exception', ex)
            return '%s' % ex

        if (jsonResponse['succes']):
            return 'OK'
        else:
            return self.convertError(jsonResponse)

    def pause(self, testID, restart):
        print('Pause', testID, restart)
        try:
            jsonResponse = self.requestUrl('/tests/%s/pause?dorestart=%s' % (testID, restart))
        except Exception as ex:
            print('Exception', ex)
            return '%s' % ex

        print('Pause', jsonResponse)
        if (jsonResponse['succes']):
            if (jsonResponse['data'] != ''):
                return jsonResponse['data']
            else:
                return 'OK'
        else:
            if (jsonResponse['messages'][0]['msgCode'] == 103):
                return 'ERROR(3): One or more parameters were missing.'
            elif (jsonResponse['messages'][0]['msgCode'] == 30012):
                return 'ERROR(12): Negative identifiers are not allowed.'
            else:
                return jsonResponse['messages'][0]

    def restarttest(self, testID):
        print('Restart', testID)
        try:
            jsonResponse = self.requestUrl('/tests/%s/restart' % (testID))
        except Exception as ex:
            print('Exception', ex)
            return '%s' % ex

        print('Pause', jsonResponse)
        if (jsonResponse['succes']):
            if (jsonResponse['data'] != ''):
                return jsonResponse['data']
            else:
                return 'OK'
        else:
            if (jsonResponse['messages'][0]['msgCode'] == 103):
                return 'ERROR(3): One or more parameters were missing.'
            elif (jsonResponse['messages'][0]['msgCode'] == 30012):
                return 'ERROR(12): Negative identifiers are not allowed.'
            else:
                return jsonResponse['messages'][0]['msgBasicContentText']

    def loadscenario(self, filePath):
        try:
            fileRead = io.open(filePath, mode="r", encoding="utf-16")
            xmlData = fileRead.read()
            fileRead.close()
            print('Str:', xmlData)
        except Exception as ex:
            if ex.args[0] == 2:
                return 'ERROR(3): One or more parameters were missing.'
            else:
                print('Exception', ex)
                return '%s' % ex

        strURLEncode = urllib.parse.quote(xmlData)
        print('strURLEncode', strURLEncode)
        data = {
            'scenario' : xmlData
        }
        try:
            jsonResponse = self.requestUrl('/scenarios/load', data, 'POST')
        except Exception as ex:
            print('Exception', ex)
            return '%s' % ex

        if (jsonResponse['succes']):
            return 'OK'
        else:
            return jsonResponse['messages'][0]

    def executescenario(self, starttime):
        try:
            print('executescenario', starttime)
            if (starttime == 0):
                jsonResponse = self.requestUrl('/scenarios/execute')
            else:
                data = {
                    'starttime': time.mktime(time.strptime(starttime, '%d-%b-%Y %H:%M:%S'))
                }
                jsonResponse = self.requestUrl('/scenarios/executeat', data, 'POST')

        except Exception as ex:
            print('Exception', ex)
            return '%s' % ex

        if (jsonResponse['succes']):
            return 'OK'
        else:
            return jsonResponse['messages'][0]

    def getresultsProfile(self, testID, profile):
        try:
            jsonResponse = self.requestUrl('/tests/%d/results' % testID, None, 'GET', {'profile': profile})
        except Exception as ex:
            print('Exception', ex)
            return '%s' % ex

        if (jsonResponse['succes']):
            return self.convertJsonToSimpleResultXML(jsonResponse['data'])
        else:
            if (jsonResponse['messages'][0]['msgCode'] == 30116):
                return 'ERROR(116): No results found matching Id.\r'
            elif (jsonResponse['messages'][0]['msgCode'] == 30115):
                return 'ERROR(115): Measure profile does not exist.\r'
            elif (jsonResponse['messages'][0]['msgCode'] == 30070):
                return 'ERROR(70): %s\r' % jsonResponse['messages'][0]['msgBasicContentText']
            else:
                return jsonResponse['messages'][0]
