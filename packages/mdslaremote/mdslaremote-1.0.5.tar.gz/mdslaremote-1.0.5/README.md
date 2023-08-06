# mdslaremote Package

This package provide a python API to user the Opale Systems MultiDSLA product remotely.

Here is a simple example of usage :

```Python
from mdslaremote import mda
import time
import datetime

def intFromStr(s):
    try:
        return int(s)
    except ValueError:
        return -1

def main():
    tasklist = 'P.501C/EN/Cellular NB/fullqualitychk.mtl'
    nodeA = 'Node A'
    nodeB = 'Node B'

    conn = (nodeA+nodeB).replace(' ', '')

    #create connectionset
    connSet = mda.addconnection(conn, nodeA, 'default', nodeB, 'default')
    print('connectionSet : {}'.format(connSet))

    #schedule test
    testid = mda.scheduletest(tasklist, conn, "1", "1", "1", mda.NOW)

    print('test ID : {}'.format(testid))

    if intFromStr(testid) != -1:
        while True:
            time.sleep(3)
            progress = mda.gettestprogress(testid)
            if progress == 'FINISHED':
                now = datetime.datetime.now()
                print('Date {}, TestId {}, Finished.'.format(str(now), testid))
                break
            else:
                if progress == 'FAILED':
                    print('Test {} is failed'.format(testid))
                    return
                else:
                    print('Test status: {}'.format(progress))
        
        # Getting PESQ results
        pesqResult = mda.getresultlist(testid, 'PESQ')
        
        print('PESQ results are : {}'.format(pesqResult))
    else:
        print('Error starting test : {}'.format(testid))


if __name__ == "__main__":
    main()
