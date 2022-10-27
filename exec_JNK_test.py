'''
Purpose:
    execute teste cases in xml format
'''
import os, sys
import socket
import time
import cPickle
import platform
import win32api
import taf_init_paths

def run_test(n_tests, n_rtests, testsetnumber, testName, projectPath, seqPath, cfgPath, testPath, repPath, repDirPath, log_file):        
    """
    ------------------------------------------------------------------------
    Description:    Executing one Test Set
    Input:          testName: the unique Name of the testset
                    projectPath: the project path (string)
                    seqPath: the test sequence filename (string)
                    cfgPath: the test configuration filename (string)
                    testPath: the test parameter filename (string)
                    repPath: the test report filename (string)
    Output:
    ------------------------------------------------------------------------
    """
    ################### Config #######################
    # location for the python executable to execute the test cases
    exe = r'c:\LegacyApp\Python27_x64\python.exe'
    HOST = '127.0.0.1'      # The remote host
    sys.stdout = log_file   # reroute the stdout to the log file    
    sys.stderr = log_file   # reroute the stderr to the log file
    ################### END Config #######################
    #print '------------- Test to execute:',  testName
    sck = None  # socket object
    conn = None # connection
    
    if(testsetnumber==0):
        print (
                '\nTM-TM-TM-TM-TM-TM-TM-TM-TM-TM-TM-TM-TM-TM-TM-TM-TM-TM\nTM\n'+
                'TM  Run started.\n' +
                'TM Server address : ' + str(platform.node()) + '\n' +
                'TM  Log File: ' +str(repPath)+"\\test_run_log.tmlog" + '\n' +
                'TM  Workspace: ' + str(projectPath.replace('D:\Projects\\','').replace('\SW_RT_Scripts','')) + '\n' +
                'TM      Project Path: ' + str(projectPath) + '\n' +
                'TM      Configuration File: ' + str(cfgPath) + '\n' +
                'TM      Report Folder Path: ' + str(repPath) + '\n' +
                'TM      Number of Workspace Test Sets: ' + str(len(n_tests)) +'\n'+
                'TM      Number of selected Workspace Test Sets: ' +
                str(len(n_rtests))+ '\n' +
                'TM\n' +
                'TM-TM-TM-TM-TM-TM-TM-TM-TM-TM-TM-TM-TM-TM-TM-TM-TM-TM\n')
    #print("run")
    try:
        import pythoncom
        pythoncom.CoInitialize()
        #print("run1")
        print (
                        '\nTM-TM-TM-TM-TM-TM-TM-TM-TM-TM-TM-TM-TM-TM-TM-TM-TM-TM\nTM\n' +
                        'TM  Test Set Number ' + str(testsetnumber) + ' starting ...\n' +
                        'TM      Test Name: ' + str(testName) + '\n'
                        'TM      Test Sequence: ' + str(seqPath) + '\n' +
                        'TM      Test Parameter: ' + str(testPath) + '\n' +
                        'TM      Test Configuration: ' + str(cfgPath) + '\n' +
                        'TM      Test Set Report File: '+str(repPath)+'\nTM\n')
        print "python version for execution = " + exe
        #print("run2")
        # searches for clientprocess.py and change directory for import
        os.chdir(os.path.dirname(taf_init_paths.findFile(projectPath, "clientprocess.py")))
        sys.path.insert(0, ".")
        # make a socket object
        sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # search for a free TCP port
        for port in xrange(49152, 65536):
            try:
                sck.bind((HOST, port))
                break
            except:                
                pass
        else:
            raise "SocketError: No Free Port found"
            
        # create the folder to store the reports
        if not os.path.exists(repDirPath):
            os.makedirs(repDirPath) 
            
        
            
        import clientprocess
        del sys.modules["clientprocess"]
        import clientprocess
        
        
    # create a new process to run the test
        print "Found old clientprocess"
        pid =  os.spawnv( os.P_NOWAIT , exe, (exe,) + \
            (" -c __import__('clientprocess').clientCaller(r'%s',r'%s',r'%s',r'%s',r'%s',r'%s',r'%s')" \
            %(projectPath, seqPath, cfgPath, testPath, repPath, port, testName) ,) )

        sck.listen(1)
        conn, addr = sck.accept()
        conn.setblocking(0)

        # waiting for process finished
        while 1:
            try:
                #print "debug run_1"
                # instead of threading
                pythoncom.PumpWaitingMessages(0, -1)
                time.sleep(0.02)

                # raised for TM1.22
                #print "debug run_2"
                data = conn.recv(int(1e5))
                #print "debug run_3"
                print data
                # test finished ?
                #if (data == "The Test has finished normally without any exceptions") or (not data):
                #if (win32event.WaitForSingleObject(FINISHED_TAF_EVENT,0) == win32event.WAIT_OBJECT_0):
                #print " debug test finished"
                if not data:
                    print "Terminated by no data"
                    break

            except socket.error, e:
                if e[0] != 10035:
                    print 
                    print "debug socket Error"
                    break
            except:
                break
    except Exception, e:
        print "no run"
        pythoncom.CoUninitialize()    
        
    else:
        try:
            # this is to make sure that no unused python processes are hanging
            # sometimes happening (reason not known)
            win32api.TerminateProcess(pid,0)
            #print" else run"
        except Exception:
            # if python process was terminated sucessfully, exception happens
            pass

        # close the socket connection
        if conn is not None:
            conn.close()
        if sck is not None:
            sck.close()
        pythoncom.CoUninitialize()
        #print "com port closed"
        # get the test result object    
        file = None
        #print "debug_1"
        picklePath = os.path.join(projectPath, r"result.pik")
        #print picklePath
        #print "debug2"
        try:
            #print "debug_3"
            file = open(picklePath, "r")
            #print "debug_4"
        except:
            executionStatus = 3
            executionEvalCount = 0
            executionEvalFailed = 0
            #traceback.print_exc(file=sys.stdout)
        else:
            result = cPickle.load(file)            
            # 0=succes
            # 3=error
            executionStatus = result.status
            executionEvalCount = result.eval_count
            executionEvalFailed = result.eval_failed
            if file is not None:
                file.close()
                # delete the pickle file to prevent wrong evaluation
                # of following repetitions
                os.unlink(picklePath)

        execStatus = 'Error'  # init value; worst case
        if executionStatus == 0:
            execStatus = 'Success'
        elif executionStatus == 1:
            execStatus = "Failed"
        elif executionStatus == 3:
            execStatus = "Error"
        return execStatus,executionEvalCount,executionEvalFailed