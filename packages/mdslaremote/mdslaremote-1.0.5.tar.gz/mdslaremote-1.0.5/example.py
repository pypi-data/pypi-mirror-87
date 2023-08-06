from mdslaremote import mda
import threading
import time
import datetime


def main():
    # Set name of Shark object
    threads = []

    start = time.time()
    # Create all the worker threads
    for i in range(0, 1):
        threads.append(threading.Thread(target=run_job, args=(i,)))
        threads[i].start()
        time.sleep(1)

    # Let the threads finish before exiting
    for i in threads:
        i.join()
    end = time.time()
    print('processing time is {}'.format(end-start))

def intFromStr(s):
    try:
        return int(s)
    except ValueError:
        return -1


def run_job(i):
    print('starting job {}'.format(i))
    starts.append(datetime.datetime.now())

    #tasklist = 'User Tasklists\\quickqualitychk_adn.mtl'
    tasklist = 'P.501C/EN/Cellular NB/fullqualitychk.mtl'
    nodeA = srcNodes[i]
    nodeB = dstNodes[i]

    conn = (nodeA+nodeB).replace(' ', '')

    connSet = mda.addconnection(conn, nodeA, 'polqa3', nodeB, 'polqa3')
    print('connectionSet : {}'.format(connSet))

    testid = mda.scheduletest(tasklist, conn, "1", "1", "1", mda.NOW)

    #testid = mda.scheduletest(tasklist, nodeA, nodeB, "3", "1", "1", mda.NOW)

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
                    print('Ending job {} Test {} is failed'.format(i, testid))
                    return
                else:
                    print('TestId {}, Test status: {}'.format(testid, progress))
        print(mda.gettestsummary(testid))
        print(mda.gettestsummary(testid, mda.BYNODE))
        # print(mda.gettestsummary(testid, 230))
        #print(mda.getresultlist(testid, 'PESQ', 'LEVELS' , 'DELAY', 'ECHO'))
        pesqResult = mda.getresultlist(testid, 'PESQ')
        elapsed = datetime.datetime.now() - starts[i - 1]
        print('PESQ results are : {}'.format(pesqResult))
        polqaResult = mda.getresultlist(testid, 'POLQA')
        print('POLQA results are : {}'.format(polqaResult))
        levelResults = mda.getresultlist(testid, 'LEVELS')
        print('LEVEL results are : {}'.format(levelResults))
        delayResults = mda.getresultlist(testid, 'DELAY')
        print('DELAY results are : {}'.format(delayResults))
        print('Ending job {} resultid is {}. Finished in {} seconds'.format(i, testid, elapsed.seconds))
    else:
        print('Error starting test : {}'.format(testid))

if __name__ == "__main__":
    starts = []
    #srcNodes = ['Les Ulis', 'Paris']
    #dstNodes = ['Montigny le Bx', 'Nanterre']
    srcNodes = ['vpp 1', 'vpp 3', 'vpp 5', 'vpp 7', 'vpp 9', 'vpp 11', 'vpp 13', 'vpp 15', 'vpp 17']
    dstNodes = ['vpp 2', 'vpp 4', 'vpp 6', 'vpp 8', 'vpp 10', 'vpp 12', 'vpp 14', 'vpp 16', 'vpp 18']
    logonsuccess = mda.logon("172.31.230.85")
    print(logonsuccess)
    mda.verbose(False)
    main()
    mda.logoff()