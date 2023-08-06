from .Common import Common as Parent
from datetime import datetime
import json
import xml.etree.ElementTree as ET


class Result(Parent):
    def getresultlist(self, testID, resulttype, eventnumber):
        try:
            jsonResponse = self.requestUrl('/tests/%s/results?resultType=%s' % (testID, resulttype))
        except Exception as ex:
            if Parent.VERBOSE:
                print('Exception', ex)
            return '%s' % ex

        if (jsonResponse['succes']):
            data = jsonResponse['data']
            y = json.loads(data)
            if Parent.VERBOSE:
                print('response y', y)
            rs = ET.Element('ResultList')
            rs.set('testID', str(y['testID']))

            dt_object = datetime.fromtimestamp(y['startTimeTS'])
            rs.set('startTime', dt_object.strftime('%Y-%m-%dT%H:%M:%S:%fZ'))

            dt_object = datetime.fromtimestamp(y['endTimeTS'])
            rs.set('endTime', dt_object.strftime('%Y-%m-%dT%H:%M:%S:%fZ'))
            for row in y['result']:
                if Parent.VERBOSE:
                    print('Result:', row)
                r = ET.Element('Result')
                r.set('ID', str(row['ID']))
                r.set('name', str(row['name']))
                r.set('type', str(row['type']))

                dt_object = datetime.fromtimestamp(row['startTimeTS'])
                r.set('startTime', dt_object.strftime('%Y-%m-%dT%H:%M:%S:%fZ'))

                dt_object = datetime.fromtimestamp(row['endTimeTS'])
                r.set('endTime', dt_object.strftime('%Y-%m-%dT%H:%M:%S:%fZ'))

                r.set('ref', str(row['reference']))
                r.set('deg', str(row['degraded']))
                for metric in row['metric']:
                    m = ET.Element('Metric')
                    m.set('type', str(metric['type']))
                    m.set('units', str(metric['units']))
                    m.text = str(metric['value'])
                    r.append(m)
                rs.append(r)
            return ET.tostring(rs)
        else:
            return jsonResponse['messages'][0]

        return '0'

    def getcallresultlist(self, callid, resulttype, measuretype):
        try:
            if (measuretype == None):
                jsonResponse = self.requestUrl('/results?callID=%s&resultType=%s' % (callid, resulttype))
            else:
                jsonResponse = self.requestUrl(
                    '/results?callID=%s&resultType=%s&measureType=%s' % (callid, resulttype, measuretype))
        except Exception as ex:
            if ('Error 30117' in str(ex)):
                return 'ERROR(3): One or more parameters were missing.\r'
            else:
                if Parent.VERBOSE:
                    print('Exception', ex)
                return '%s' % ex
        if Parent.VERBOSE:
            print('getcallresultlist', jsonResponse)
        if (jsonResponse['succes']):
            XML = self.convertResultJsonToXML(jsonResponse['data'])
            if Parent.VERBOSE:
                print('XML', XML)
            return XML
        else:
            if Parent.VERBOSE:
                print('Messages', jsonResponse['messages'][0])
            if (jsonResponse['messages'][0]['msgCode'] == 30117):
                return 'ERROR(3): One or more parameters were missing.\r'
            elif (jsonResponse['messages'][0]['msgCode'] == 30116):
                return 'Error 30116: No result found.'
            else:
                return jsonResponse['messages'][0]

        return '0'

    def getmeasuretypes(self):
        try:
            jsonResponse = self.requestUrl('/tests/measureTypes')
        except Exception as ex:
            if Parent.VERBOSE:
                print('Exception', ex)
            return '%s' % ex

        if (jsonResponse['succes']):
            data = jsonResponse['data']
            return data
        else:
            return jsonResponse['messages'][0]

    def getmeasureprofiles(self):
        try:
            jsonResponse = self.requestUrl('/tests/profiles')
        except Exception as ex:
            if Parent.VERBOSE:
                print('Exception', ex)
            return '%s' % ex

        if (jsonResponse['succes']):
            data = jsonResponse['data']
            return data
        else:
            return jsonResponse['messages'][0]

    def getresultProfile(self, resultID, profile):
        try:
            jsonResponse = self.requestUrl('/results/%d' % resultID, None, 'GET', {'profile': profile})
        except Exception as ex:
            if Parent.VERBOSE:
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

    def getresultidfromdegpath(self, fileName):
        try:
            jsonResponse = self.requestUrl('/results', None, 'GET', {'filename': fileName})
        except Exception as ex:
            if Parent.VERBOSE:
                print('Exception', ex)
            return '%s' % ex

        if (jsonResponse['succes']):
            return jsonResponse['data']
        else:
            if (jsonResponse['messages'][0]['msgCode'] == 30116):
                return 'ERROR(116): No results found matching Id.\r'
            elif (jsonResponse['messages'][0]['msgCode'] == 30115):
                return 'ERROR(115): Measure profile does not exist.\r'
            elif (jsonResponse['messages'][0]['msgCode'] == 30070):
                return 'ERROR(70): %s\r' % jsonResponse['messages'][0]['msgBasicContentText']
            elif (jsonResponse['messages'][0]['msgCode'] == 30111):
                return 'ERROR(111): %s' % jsonResponse['messages'][0]['msgBasicContentText']
            else:
                return jsonResponse['messages'][0]

    def gettestsummary(self, testID, bynode):
        try:
            jsonResponse = self.requestUrl('/results?testid=%s&summary=True' % testID)
        except Exception as ex:
            if Parent.VERBOSE:
                print('Exception', ex)
            return '%s' % ex

        if (jsonResponse['succes']):
            XML = self.convertSummaryJsonToXML(jsonResponse['data'])
            if Parent.VERBOSE:
                print('XML', XML)
            return str(XML)
        else:
            if (jsonResponse['messages'][0]['msgCode'] == 30116):
                return 'ERROR(116): No results found matching Id.\r'
            elif (jsonResponse['messages'][0]['msgCode'] == 30115):
                return 'ERROR(115): Measure profile does not exist.\r'
            elif (jsonResponse['messages'][0]['msgCode'] == 30070):
                return 'ERROR(70): %s\r' % jsonResponse['messages'][0]['msgBasicContentText']
            elif (jsonResponse['messages'][0]['msgCode'] == 30111):
                return 'ERROR(111): %s' % jsonResponse['messages'][0]['msgBasicContentText']
            else:
                return jsonResponse['messages'][0]

    def exportreporttofile(self, *args):
        if Parent.VERBOSE:
            print("Export arguments", args)
        report = ''
        fileType = 'CSV'
        period = 'CURRENT'

        if (args[0] == -1):
            report = 'SUMMARY'
        elif (args[0] == -2):
            report = 'CONNECTIONS'
        elif (args[0] == -3):
            report = 'TREND'
        elif (args[0] == -4):
            report = 'KPI'

        if (len(args) > 5):
            pathName = args[6]
        else:
            pathName = args[3]
        if Parent.VERBOSE:
            print('Path name', type(pathName), len(pathName), pathName)
        if (len(pathName) > 3):
            ext = pathName[len(pathName) - 3:]
            if (ext == 'CSV' or ext == 'TXT' or ext == 'XML' or ext == 'KMZ'):
                fileType = ext

        if (len(args) > 5):
            if (args[3] == mda.ALLNODES):
                node = "ALLNODES"
            else:
                node = args[3]

            parameter = {
                'user': args[2],
                'node': node,
                'type': fileType,
                'report': report,
                'profile': args[1],
            }

            if (type(args[5]) is int):
                if (args[5] == -1):
                    period = 'MINUTES'
                elif (args[5] == -2):
                    period = 'HOURS'
                elif (args[5] == -3):
                    period = 'DAYS'
                elif (args[5] == -4):
                    period = 'WEEKS'

                parameter['period'] = period
                parameter['range'] = args[4]
            # elif (type(args[5]) is str):
            else:
                # "%Y-%m-%d %H:%M:%S"
                datetime_from = datetime.strptime(args[4], '%d-%b-%Y %H:%M:%S')
                periodFrom = datetime_from.timestamp()
                datetime_to = datetime.strptime(args[5], '%d-%b-%Y %H:%M:%S')
                periodTo = datetime_to.timestamp()

                parameter['periodFrom'] = periodFrom
                parameter['periodTo'] = periodTo
        else:
            parameter = {
                'testid': args[2],
                'type': fileType,
                'report': report,
                'profile': args[1],
                'period': period,
            }
        if (len(args) > 4):
            if (args[4] == mda.UNICODE):
                parameter['switch'] = '-UNICODE'
            elif (args[4] == mda.V1TO3):
                parameter['switch'] = 'V1TO3'

        try:
            jsonResponse = self.requestUrl('/results/export', None, 'GET', parameter)
        except Exception as ex:
            if Parent.VERBOSE:
                print('Exception', ex)
            return '%s' % ex

        if (jsonResponse['succes']):
            if Parent.VERBOSE:
                print('Try print file', pathName)
            file = open(pathName, "w")  # Argh j'ai tout écrasé !
            file.write(jsonResponse['data'].replace('\r\n', '\n'))
            file.close()

            return 'OK'
        else:
            if (jsonResponse['messages'][0]['msgCode'] == 30116):
                return 'ERROR(116): No results found matching Id.\r'
            elif (jsonResponse['messages'][0]['msgCode'] == 30115):
                return 'ERROR(115): Measure profile does not exist.\r'
            elif (jsonResponse['messages'][0]['msgCode'] == 30070):
                return 'ERROR(70): %s\r' % jsonResponse['messages'][0]['msgBasicContentText']
            elif (jsonResponse['messages'][0]['msgCode'] == 30111):
                return 'ERROR(111): %s' % jsonResponse['messages'][0]['msgBasicContentText']
            elif (jsonResponse['messages'][0]['msgCode'] == 30130):
                return 'ERROR(130): %s' % jsonResponse['messages'][0]['msgBasicContentText']
            elif (jsonResponse['messages'][0]['msgCode'] == 30012):
                return 'ERROR(12): %s' % jsonResponse['messages'][0]['msgBasicContentText']
            elif (jsonResponse['messages'][0]['msgCode'] == 30017):
                return 'ERROR(17): %s' % jsonResponse['messages'][0]['msgBasicContentText']
            else:
                return jsonResponse['messages'][0]
