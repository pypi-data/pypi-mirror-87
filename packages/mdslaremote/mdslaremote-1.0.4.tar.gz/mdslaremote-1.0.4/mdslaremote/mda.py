from .impl import Mdsla as Console
from .impl import Common as Constants

mdsla = None


def logon(address, username=None, password=None, port=8082):
    global mdsla
    mdsla = Console.Mdsla(address, port)
    print('mdsla 1:', mdsla)
    return mdsla.login(address, port, username, password)


def logoff():
    global mdsla
    mdsla.logoff()
    return True


def geteol():
    return mdsla.geteol()


def seteol(eol):
    return mdsla.seteol(eol)


def getsystemtime():
    global mdsla
    return mdsla.getsystemtime()


def getsystemutctime():
    global mdsla
    return mdsla.getsystemutctime()


def getuptime():
    global mdsla
    return mdsla.getuptime()


def getnodelist():
    global mdsla
    print('mdsla 2:', mdsla)
    nodes = mdsla.node.getAll()
    print('Nodes:', nodes)
    result = None
    for node in nodes:
        if result == None:
            result = node['name']
        else:
            result = '%s;%s' % (result, node['name'])
    return result
    return mdsla.node.getAll()


def addnode(basename, nodetype, address, groupname=None, quantity=1, polqa=False):
    return mdsla.node.add(basename, nodetype, address, polqa, groupname, quantity)


def deletenode(nodename):
    return mdsla.node.delete(nodename)


def copynode(srcnode, destnode, ipaddress):
    return mdsla.node.copy(srcnode, destnode, ipaddress)


def getnodetypelist():
    return mdsla.node.getTypes()


def restorenodes(fileName):
    return mdsla.node.importFile(fileName)


def checkstatus(nodename):
    return mdsla.node.getStatus(nodename)


# doublon
def nodereset(nodename):
    return mdsla.node.reset(nodename)


def reset(nodename):
    return mdsla.node.reset(nodename)


def setconfigparam(nodeName, configName, ParamName, value):
    return mdsla.node.setconfigparam(nodeName, configName, ParamName, value)


def getconfigparam(nodeName, configName, ParamName):
    return mdsla.node.getconfigparam(nodeName, configName, ParamName) + mdsla.GetEndOfLine()


def getnodeversion(nodename):
    return mdsla.node.getVersion(nodename)


def isrunningtest(nodename):
    return mdsla.node.isRunningTest(nodename)


def clearfilesystem(nodename):
    return mdsla.node.clearfilesystem(nodename)


def getfsclrtimeout():
    return mdsla.node.getfsclrtimeout()


def setfsclrtimeout(timeout):
    return mdsla.node.setfsclrtimeout(timeout)


def getconfiglist(nodename):
    return mdsla.node.getConfigurations(nodename)


def getversion():
    return mdsla.getVersion()


def getgroups():
    groups = mdsla.group.getAll()
    print('getgroups', groups)
    result = None
    for group in groups:
        print('getgroup', group)
        if result == None:
            result = group['name']
        else:
            result = '%s;%s' % (result, group['name'])
    return result


def getgroupnodes(groupName):
    nodes = mdsla.node.getAll()
    result = None
    for node in nodes:
        if node['groupName'] == groupName:
            if result == None:
                result = node['name']
            else:
                result = '%s;%s' % (result, node['name'])
    return result


def upgradefirmware(nodename, path):
    return mdsla.node.upgradefirmware(nodename, path)


def scheduletest(mtlName, *args):
    print('Args', args)
    if (len(args) > 5):
        return mdsla.test.schedule(mtlName, args[0], args[1], args[2], args[3], args[4], args[5])
    else:
        return mdsla.test.schedule(mtlName, args[0], args[1], args[2], args[3], args[4])


# def scheduletest(mtlName, nodeA, nodeB, executes, calls, period, starttime):
#    return mdsla.test.schedule(mtlName, nodeA, nodeB, executes, calls, period, starttime)

def starttest(mtlName, *args):
    print('Args', args, len(args))
    if (len(args) == 1):
        return mdsla.test.start(mtlName, args[0])
    elif (len(args) == 2):
        return mdsla.test.start(mtlName, args[0], args[1])
    else:
        return 'KO'


def stoptest(testID):
    return mdsla.test.stop(testID)


def terminatealltests():
    return mdsla.test.terminateall()


def getresultlist(testID, resulttype, eventnumber=None):
    return mdsla.test.getresultlist(testID, resulttype, eventnumber)


def getcurrenttestlist():
    return mdsla.test.getcurrenttestlist()


def getfuturetestlist():
    return mdsla.test.getfuturetestlist()


def getrunningtestlist():
    return mdsla.test.getrunningtestlist()


# def getmeasuretypes(callid, resulttype, measuretype=None):
#     return mdsla.result.getmeasuretypes(callid, resulttype, measuretype)

def getmeasuretypes():
    return mdsla.test.getmeasuretypes()


def getcallresultlist():
    return mdsla.result.getcallresultlist()


def getcallresultlist(callid, resulttype, measuretype=None):
    return mdsla.result.getcallresultlist(callid, resulttype, measuretype)


def getcallssincetest(testid, callid):
    return mdsla.call.getcallssincetest(testid, callid)


def addconnection(connectionset, nodeA, configA, nodeB, configB):
    return mdsla.connection.addconnection(connectionset, nodeA, configA, nodeB, configB)


def removeconnection(connectionset):
    return mdsla.connection.removeConnection(connectionset)


def gettestprogress(testID):
    return mdsla.test.gettestprogress(testID)


def getcallprogress(callID):
    return mdsla.call.getcallprogress(callID)


def getnextcallstart(testID):
    return mdsla.call.getnextcallstart(testID)


def terminatetest(testID):
    return mdsla.test.terminatetest(testID)


def pausetest(testID, restart=False):
    if (restart == '-RESTART'):
        restart = True
    else:
        restart = False
    return mdsla.test.pause(testID, restart)


def restarttest(testID):
    return mdsla.test.restarttest(testID)


def loadscenario(file):
    return mdsla.test.loadscenario(file)


def executescenario():
    return mdsla.test.executescenario(0)


def executescenarioat(starttime):
    return mdsla.test.executescenario(starttime)


def gettestlist():
    return mdsla.test.getTaskListFile()


def seteventlogpathname(path):
    return mdsla.seteventlogpathname(path)


def uploadtasklist(fileName, data):
    return mdsla.taskList.upload(fileName, data)


def getmeasureprofiles():
    return mdsla.result.getmeasureprofiles()


def getmeasuresbytestid(testid, profile):
    return mdsla.test.getresultsProfile(testid, profile)


def getmeasuresfromresultid(resultID, profile):
    return mdsla.result.getresultProfile(resultID, profile)


def getresultidfromdegpath(fileName):
    return mdsla.result.getresultidfromdegpath(fileName)


def gettestsummary(testID, bynode=0):
    return mdsla.result.gettestsummary(testID, bynode)


def exportreporttofile(*args):
    return mdsla.result.exportreporttofile(*args)


NO_PORT = Constants.Common.NO_PORT
MDA_PORT = Constants.Common.MDA_PORT
DEFAULT_PORT = Constants.Common.MDA_PORT
NOCALL = Constants.Common.NOCALL
INCALLSETUP = Constants.Common.INCALLSETUP
ACTIVECALL = Constants.Common.ACTIVECALL
CALLDROPPED = Constants.Common.CALLDROPPED
CALLFAILED = Constants.Common.CALLFAILED
WAITING = Constants.Common.WAITING
RUNNING = Constants.Common.RUNNING
FINISHED = Constants.Common.FINISHED
FAILED = Constants.Common.FAILED
POLQA = Constants.Common.POLQA
BYNODE = Constants.Common.BYNODE
NOW = Constants.Common.NOW
ALLCALLS = Constants.Common.ALLCALLS
INCWAITING = Constants.Common.INCWAITING
SUMMARY = Constants.Common.SUMMARY
CONNECTIONS = Constants.Common.CONNECTIONS
TREND = Constants.Common.TREND
KPI = Constants.Common.KPI
ALLUSERS = Constants.Common.ALLUSERS
ALLNODES = Constants.Common.ALLNODES
CURRENT = Constants.Common.CURRENT
TODATE = Constants.Common.TODATE
MINUTES = Constants.Common.MINUTES
HOURS = Constants.Common.HOURS
DAYS = Constants.Common.DAYS
WEEKS = Constants.Common.WEEKS
UNICODE = Constants.Common.UNICODE
V1TO3 = Constants.Common.V1TO3

if __name__ == '__main__':
    print(getnodelist())
