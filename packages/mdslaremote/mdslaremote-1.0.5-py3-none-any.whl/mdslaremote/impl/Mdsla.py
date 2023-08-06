from datetime import datetime

from .Call import Call
from .ConnectionSet import ConnectionSet
from .Group import Group
from .Node import Node
from .Result import Result
from .TaskList import TaskList
from .Test import Test

from .Common import Common


class Mdsla(Common):
    userId = None
    node = None
    group = None
    _EOL = 'CR'

    def __init__(self, host=None, port=80, version='v1'):
        super().__init__(host, port, version)
        self.initManager(host, port, version)

    def initManager(self, host, port, version):
        self.node = Node(host, port, version)
        self.group = Group(host, port, version)
        self.test = Test(host, port, version)
        self.result = Result(host, port, version)
        self.call = Call(host, port, version)
        self.connection = ConnectionSet(host, port, version)
        self.taskList = TaskList(host, port, version)

    def GetEndOfLine(self):
        if self._EOL == 'CR':
            return '\r'
        elif self._EOL == 'LF':
            return '\n'
        elif self._EOL == 'CRLF':
            return '\r\n'

        return '\r'

    def getVersion(self):
        # /info/version
        try:
            jsonResponse = self.requestUrl('/infos/version')
        except Exception as ex:
            if Common.VERBOSE:
                print('Exception:', ex)
            return '%s' % ex

        if (jsonResponse['succes']):
            version = jsonResponse['data']
            versionList = version.split('.')
            if Common.VERBOSE:
                print('Get Version', version, versionList)
            if len(versionList) != 4:
                return jsonResponse['data']
            else:
                return '%s.%s.%s (%s)%s' % (
                versionList[0], versionList[1], versionList[2], versionList[3], self.GetEndOfLine())
        else:
            return jsonResponse['messages'][0]

    def login(self, host, port, username, password):
        if Common.VERBOSE:
            print('Connection:', host, port)
        self.host = host
        self.port = port

        try:
            jsonResponse = self.requestUrl('/connection/logon')
        except Exception as ex:
            if Common.VERBOSE:
                print('Exception:', ex)
            return '%s' % ex

        self.userId = jsonResponse['data']

        self.initManager(host, port, self.version)
        if (jsonResponse['succes']):
            return 'OK'
        else:
            return jsonResponse['messages'][0]

    def logoff(self):
        self.userId = None
        return True

    def geteol(self):
        return self._EOL + self.GetEndOfLine()

    def seteol(self, eol):
        if eol == 'CR' or eol == 'LF' or eol == 'CRLF':
            self._EOL = eol
            return 'OK'
        else:
            return 'ERROR(4): One or more parameters were of an invalid type or value.'

    def getsystemtime(self):
        try:
            jsonResponse = self.requestUrl('/infos/systemTime')
        except Exception as ex:
            if Common.VERBOSE:
                print('Exception:', ex)
            return '%s' % ex

        if (jsonResponse['succes']):
            if Common.VERBOSE:
                print('json time', jsonResponse['data'])
            value = jsonResponse['data'].replace(',', '.')
            dt_object = datetime.fromtimestamp(float(value))
            return dt_object.strftime('%d/%m/%Y %H:%M:%S') + self.GetEndOfLine()
        else:
            return jsonResponse['messages'][0]

    def getsystemutctime(self):
        try:
            jsonResponse = self.requestUrl('/infos/systemUtcTime')
        except Exception as ex:
            if Common.VERBOSE:
                print('Exception:', ex)
            return '%s' % ex

        if (jsonResponse['succes']):
            if Common.VERBOSE:
                print('json time', jsonResponse['data'])
            value = jsonResponse['data'].replace(',', '.')
            dt_object = datetime.fromtimestamp(float(value))
            return dt_object.strftime('%d/%m/%Y %H:%M:%S') + self.GetEndOfLine()
        else:
            return jsonResponse['messages'][0]

    def getuptime(self):
        try:
            jsonResponse = self.requestUrl('/infos/upTime')
        except Exception as ex:
            if Common.VERBOSE:
                print('Exception:', ex)
            return '%s' % ex

        if (jsonResponse['succes']):
            if Common.VERBOSE:
                print('json time', jsonResponse['data'])
            return jsonResponse['data'] + self.GetEndOfLine()
        else:
            return jsonResponse['messages'][0]

    def seteventlogpathname(self, path):
        try:
            data = {
                'value': path,
                'defaultValue': '',
                'userid': self.userId
            }
            jsonResponse = self.requestUrl('/systemsetting/PathEventLog', data, 'PATCH')
        except Exception as ex:
            if Common.VERBOSE:
                print('Exception:', ex)
            return '%s' % ex

        if (jsonResponse['succes']):
            return 'OK'
        else:
            return jsonResponse['messages'][0]
