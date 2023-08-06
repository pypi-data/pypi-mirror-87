import urllib.request
import json
from datetime import datetime
import xml.etree.ElementTree as ET


class Common(object):
    #static fields
    VERBOSE = False
    NO_PORT = -1
    MDA_PORT = 8082
    DEFAULT_PORT = MDA_PORT
    NOCALL = 0
    INCALLSETUP = 1
    ACTIVECALL = 2
    CALLDROPPED = -1
    CALLFAILED = -2
    WAITING = 1
    RUNNING = 2
    FINISHED = 0
    FAILED = -1
    POLQA = -1
    BYNODE = -1
    NOW = -1
    ALLCALLS = -1
    INCWAITING = -1
    SUMMARY = -1
    CONNECTIONS = -2
    TREND = -3
    KPI = -4
    ALLUSERS = -1
    ALLNODES = -1
    CURRENT = -1
    TODATE = -2
    MINUTES = -1
    HOURS = -2
    DAYS = -3
    WEEKS = -4
    UNICODE = -1
    V1TO3 = -2

    #attributes
    host = None
    version = 'v1'
    address = None
    port = 80

    def __init__(self, host = None, port = 80, version = 'v1'):
        self.host = host
        self.port = port
        self.version = version
        self.address = 'http://%s:%d/api/%s' % (self.host, self.port, self.version)

    # return url
    def getUrl(self, path):
        return '%s%s' % (self.address, path)

    def requestUrl(self, path, data = None, method = 'GET', queryParams = None):
        dataEncode = None
        html = None
        if queryParams != None:
            path = '%s?%s'  % (path, urllib.parse.urlencode(queryParams))
        url = self.getUrl(path)
        if Common.VERBOSE:
            print('URL:', url, 'Data:', data, 'Method:', method)
        try:
            if (data != None):
                dataEncode = urllib.parse.urlencode(data)
                dataEncode = dataEncode.encode('utf-8')

            req = urllib.request.Request(url, data=dataEncode, method=method)
            with urllib.request.urlopen(req) as response:
                html = response.read()

        except urllib.error.HTTPError as err:
            html = err.read()
            if Common.VERBOSE:
                print('Reads:', html)
            jsonResponse = json.loads(html.decode())
            if (not 'succes' in jsonResponse or not 'messages' in jsonResponse):
                raise Exception('The Rest API doesn\'t return a Json message: %s' % jsonResponse)
            else:
                return jsonResponse
                #raise Exception('Error %s: %s' % (jsonResponse['messages'][0]['msgCode'], jsonResponse['messages'][0]['msgContentText']))

        except Exception as ex:
            if (len(ex.args) > 0):
                raise Exception('%s' % ex.args[0])
            else:
                raise Exception('%s' % ex)

        jsonResponse = json.loads(html.decode())
        if (not 'succes' in jsonResponse or not 'data' in jsonResponse):
            raise Exception('The Rest API doesn\'t return a Json message: %s' % jsonResponse)

        return jsonResponse

    def convertSummaryJsonToXML(self, data):
        y = json.loads(data)
        if Common.VERBOSE:
            print('response y', type(y), len(y), y)
        rs = ET.Element('ResultSummary')
        rs.set('testID', str(y['testID']))
        rs.set('testName', str(y['testName']))

        dt_object = datetime.fromtimestamp(y['startTimeTS'])
        rs.set('startTime', dt_object.strftime('%Y-%m-%dT%H:%M:%S:%fZ'))
        dt_object = datetime.fromtimestamp(y['endTimeTS'])
        rs.set('endTime', dt_object.strftime('%Y-%m-%dT%H:%M:%S:%fZ'))

        for row in y['metrics']:
            if Common.VERBOSE:
                print('Metrics:', row)
            m = ET.Element('Metric')
            m.set('type', str(row['name']))
            m.set('units', str(row['units']))

            avg = ET.Element('Average')
            avg.text = str(row['average'])
            m.append(avg)

            min = ET.Element('min')
            min.text = str(row['min'])
            m.append(min)

            max = ET.Element('max')
            max.text = str(row['max'])
            m.append(max)

            rs.append(m)
        return ET.tostring(rs, encoding='unicode')

    def convertResultJsonToXML(self, data):
        y = json.loads(data)
        if Common.VERBOSE:
            print('response y', type(y), len(y), y)
        if (len(y) == 0): return ''
        rs = ET.Element('ResultSummary')
        rs.set('testID', str(y['testID']))

        dt_object = datetime.fromtimestamp(y['startTimeTS'])
        rs.set('startTime', dt_object.strftime('%Y-%m-%dT%H:%M:%S:%fZ'))

        dt_object = datetime.fromtimestamp(y['endTimeTS'])
        rs.set('endTime', dt_object.strftime('%Y-%m-%dT%H:%M:%S:%fZ'))
        for row in y['result']:
            if Common.VERBOSE:
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

        #encode to unicode to have a str class and not a bytes
        return ET.tostring(rs, "unicode")

    def convertJsonToSimpleResultXML(self, data):
        y = json.loads(data)
        if Common.VERBOSE:
            print('response y', type(y), len(y), y)
        if (len(y) == 0): return ''
        rs = ET.Element('results')
        for row in y['result']:
            if Common.VERBOSE:
                print('Result:', row)

            for metric in row['metric']:
                m = ET.Element('result')
                m.set('type', str(metric['type']))
                m.set('units', str(metric['units']))
                m.text = str(metric['value'])
                rs.append(m)

        #encode to unicode to have a str class and not a bytes
        return ET.tostring(rs, "unicode").replace('>', '>\r\n')