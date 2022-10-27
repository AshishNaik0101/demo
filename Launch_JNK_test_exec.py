import os.path
import time
import logging
import datetime 
from pytz import timezone
import os, sys, stat
import exec_JNK_test
import taf_init_paths
import xml.etree.ElementTree as ET 
import platform

################### Read parameters from command line #######################
repResults = sys.argv[1].strip()    # reporting path from jenkins call
build_name = sys.argv[2].strip()    # read build name from jenkins call
try:  
    git_commit_id = sys.argv[3].strip()    # read commit id from jenkins call
except:
    git_commit_id="tbd"
test=1


if not os.path.isfile("D://Jenkins//flag.txt"):
    print 'The file does not exist!'
else:
    f=open("D://Jenkins//flag.txt","r")
    string=str(f.readline())
    if string == 'run' :
        print 'run'

        
        
        #print repResults
        #print build_name

        ################### Config #######################
        # paths configuration
        projectPath = r'd:\Projects\VWH020Z0' #the path for the project folder
        testsPath = r'd:\Projects\VWH020Z0\work\ta\project\tests' #path for the folder with tests 
        #seqPath = r'd:\Projects\EMR4\SWRT_Scripts\EMR4_TA\work\ta\contest\taf\ta2\seq\sequencetest.py'  py script to interpret the content of xml file
        seqPath=r'd:\Projects\VWH020Z0\work\ta\ta2\seq\unifiedtest.py'
        cfgPath = r'd:\Projects\VWH020Z0\work\ta\project\cnf\prjconfig_SCLX.xml'   # platform startup configurations
        cfgPath1 = r'd:\Projects\VWH020Z0\work\ta\project\cnf\prjconfig_SCLX.xml'   #INca DB
        cfgPath2 =  r'd:\Projects\VWH020Z0\work\ta\project\cnf\prjconfig_SCLX.xml'  #sw FLash
        flash_bat_file = r'C:\Users\uidv8582\Desktop\TLP7.2.0_IFX_USB.bat'
        out_path = r'd:\Jenkins\FLASH\Path_to_SW_to_be_flashed.txt' # paht of the file that contains the current build path
        Test_run_file =  r'd:\Jenkins\FLASH\Test_run.txt'
        uutinfo_file = r'd:\Projects\VWH020Z0\work\ta\project\cnf\cnf_uut_info.xml'
        dst=r'd:\Jenkins\FLASH\VWH020Z0'
        sw_path_txt=r'd:\Jenkins_Flash\Jenkins_Flash.txt'
        ################### END Config ######################
 
        ################### END Read parameters from command line #######################
        #############################Report variables ##################
        Test_execResult=""
        Test_executionEvalCount=""
        Test_executionEvalFailed=""

        ##########################################unused code#######################

        f=open(sw_path_txt)
        sw=f.read().splitlines()
        sw_path=sw[0].strip()+"\\"+"developer_build\\VWH02__60B_unsigned\\VWH02\\code"
        f.close()
        print(sw_path)
        L_files=os.listdir(sw_path.replace("code", "inca"))        
        for n in range(len(L_files)):
            if("VWH02_60B_Cal.s19" == L_files[n] or "VWH02_60B_Cal.S19" == L_files[n] or "VWH02_60B_Cal.s19" == L_files[n] or "VWH02_60B_Cal.S19" == L_files[n]):
                ASW_Cal_path=sw_path.replace("code", "inca")+"\\"+L_files[n]
            if("VWH02_60B.a2l" == L_files[n] or "VWH02_60B.A2L" == L_files[n] or "VWH02_60B.a2l" == L_files[n] or "VWH02_60B.A2L" == L_files[n]):
                a2l_path=sw_path.replace("code", "inca")+"\\"+L_files[n]
        f=open(out_path,'w')
        f.writelines(sw_path)
        f.writelines("\n"+a2l_path)
        f.writelines("\n"+ASW_Cal_path)
        f.close()
        sw_name=sw_path.split('\\')[2]

        ################### Update flash.bat with the code to flash #######################

        ################### END Update flash.bat #######################

        #####################UUT info update ###########################
        def update_uut_info():
            os.chmod(uutinfo_file, stat.S_IWRITE)
            # importing element tree

            # Pass the path of the xml document 
            tree = ET.parse(uutinfo_file)
            # get the parent tag 
            root = tree.getroot()
            print ("Software Name : " + sw_name)
            print ("Build Name : " + build_name)
            print ("GIT Commit ID : " + git_commit_id)
            root[4][1].text=sw_name+"_"+build_name+"_"+git_commit_id
            root[13][1].text = "TLS01 Scalexio VIII"
	    root[5][1].text = git_commit_id
            try: 
                if("CommitID" in root[5][0].text):
                    root[5][1].text=git_commit_id
                    root[11][1].text="tbd"
                    root[12][1].text="tbd"
                    root[13][1].text="tbd"
                    root[14][1].text=str(platform.node())
                    root[15][1].text="tbd"
                    root[16][1].text="Jenkins Run"
                    print("1 : "+ root[16][0].text)
                    print("2 : "+ root[16][1].text)
                else:
                    root[15][1].text="Jenkins Run"
            except: 
                print("CommitID is not available in info File") 
            #updated  values are printed
            print("3 :"+ root[4][0].text)
            print("4 :"+ root[4][1].text)
            print("5 :"+ root[5][0].text)
            print("6 :"+ root[5][1].text)
	    print("7 :"+ root[13][0].text)
	    print("8 :"+ root[13][1].text)
            print("9 :"+ root[14][0].text)
            print("10 :"+ root[14][1].text)
            print("11 :"+ root[15][0].text)
            print("12 :"+ root[15][1].text)
            tree.write(uutinfo_file,encoding = "UTF-8", xml_declaration = True)
        update_uut_info()
        
        ###############################################################

        ################### Create Reports folder #######################
        # reports folder for current test run_test
        
        repPath = repResults +'\\'+ build_name + '\HIL_TestsReports'

        # create the folder to store the reports
        if not os.path.exists(repPath):
            os.makedirs(repPath) 
        ################### END Create Reports folder #######################    
            
        ################### Prepare Test Log and Test Status files #######################    
        # configure test log execution and bind it to stdout
        exec_log_file_path = repPath + '\\test_run_log.tmlog'
        exec_log_file = open(exec_log_file_path, 'w')
        sys.sdtout = exec_log_file
        sys.stderr = exec_log_file
        # prepare tests status file 
        TestExecResult = open(repPath +'\TestExecResult.txt', 'w')
        execResults = []
        ################### END Prepare Test Log #######################  

        ################### Read Jenkins Tests folder content ####################### 
        FoldersList=[]
        TestList=[]
        TestsList=[]
        PathsList = []
        PathsList_run=[]
        Tests_run=[]
        FoldersList.append(testsPath)
        def read_folders_struct(FoldersList):
                lista_curenta = os.listdir(FoldersList[0])
                for element in lista_curenta:
                    if element[-4:len(element)] == '.xml':
                            PathsList.append(FoldersList[0]+'\\'+element)
                            TestList.append(element)
                    elif element.find('.')==-1:
                        FoldersList.append(FoldersList[0]+'\\'+element)
                del FoldersList[0]
                
        while (FoldersList):
            read_folders_struct(FoldersList)
        ################### END Read Jenkins Tests ####################### 

        #########################READ Test_run.txt to run tests which are present ###############
        f=open(Test_run_file,'r')
        Tests_run = f.read().splitlines()
        f.close()
        #print(TestList)
        for run in range(len(Tests_run)):
            for test in range(len(TestList)):
                if((Tests_run[run].lower()+".xml")== (TestList[test].lower())):
                    TestsList.append(TestList[test])
                    PathsList_run.append(PathsList[test])        #if(Test_run_file==""):
        #   TestsList=TestList
        #    PathsList_run=PathsList
        #   print("all test cases are selected")
        print("Test list")
        print("Numer of tets to be executed "+str(len(TestsList)))
        print("Number of tests in tests folder "+str(len(TestList)))
        #print(TestList)
        print("Test list selected")
        print(TestsList)
        #print(TestList)
        print("Tests run list")
        print(Tests_run)
        #print(PathsList_run+"dfh")
        ##################TM LOG ########################################
         
        totalT = 0   

        ################### INCA DB set up  ####################### 
        inca_test_name = 'Inca_DBset_up.xml'
        t = time.clock() 
        try:
            inca_test_idx = TestsList.index(inca_test_name)
            inca_test_path = r'%s' %(PathsList_run[inca_test_idx])

            # remove the flashing test from tests to execute list
            del TestsList[inca_test_idx]
            del PathsList_run[inca_test_idx]
            print("INCA DB")
            # configure test reporting paths
            repTestPath = repPath + '\\'+ inca_test_name.split('.')[0] +'\\' + inca_test_name
            print '------------------ repTestPath', repTestPath
            repDirPath = repPath + '\\' + inca_test_name.split('.')[0]
            print '------------------ repDirPath', repDirPath
            # run flash test
            Test_execResult,Test_executionEvalCount,Test_executionEvalFailed = exec_JNK_test.run_test(n_tests =TestList,n_rtests = Tests_run, testsetnumber = inca_test_idx, testName = inca_test_name.split('.')[0], projectPath = projectPath, seqPath = seqPath, cfgPath =cfgPath1, testPath = inca_test_path, repPath = repTestPath, repDirPath = repDirPath, log_file = exec_log_file) 
            #print("not flash")
            #print ('\nTM\nTM  Test Set Number ' +str(tst_idx) + ' finished.\n'+ 'TM      Test Execution Time: ' + str(t) + ' s\n'+'TM      Test Result: ' + str(Test_execResult) + 'TM      Number of executed tests: ' + str(tst_idx) + ' / ' + str(len(PathsList_run)) + '\nTM\n'+'TM-TM-TM-TM-TM-TM-TM-TM-TM-TM-TM-TM-TM-TM-TM-TM-TM-TM\n')

        except (NameError, ValueError), e:
            print '--> Exception !!!'
            print 'Inca_DBset_up.xml is not available into tests folder. Consequently the SW flashing is not possbile'
        except :
            print 'Exception occurred during flashing process !!'
        t = int((time.clock() - t) * 100) / 100.0
        totalT += t
        print(Test_execResult)
        # store test execution result 
        testResult = [inca_test_name.split('.')[0], Test_execResult, Test_executionEvalCount, Test_executionEvalFailed]
        execResults.append(testResult)
        print('\nTM\nTM  Test Set Number ' +str(inca_test_idx) + ' finished.\n' + 
                        'TM      Test Execution Time: ' + str(t) + ' s\n'
                        'TM      Test Result: ' + str(Test_execResult) + '\n' + 
                        'TM      Number of executed tests: ' + str(inca_test_idx) + ' / ' + str(len(PathsList_run)-1) + '\nTM\n' + 
                        'TM-TM-TM-TM-TM-TM-TM-TM-TM-TM-TM-TM-TM-TM-TM-TM-TM-TM\n')
        ################### END INCA DB #######################
        
        ################### Flash new SW checkpoint ####################### 
        flash_test_name = 'SW_Flash_Trace32.xml'
        t = time.clock() 
        try:
            flash_test_idx = TestsList.index(flash_test_name)
            flash_test_path = r'%s' %(PathsList_run[flash_test_idx])

            # remove the flashing test from tests to execute list
            del TestsList[flash_test_idx]
            del PathsList_run[flash_test_idx]
            print("FLash")
            # configure test reporting paths
            repTestPath = repPath + '\\'+ flash_test_name.split('.')[0] +'\\' + flash_test_name
            print '------------------ repTestPath', repTestPath
            repDirPath = repPath + '\\' + flash_test_name.split('.')[0]
            print '------------------ repDirPath', repDirPath
            # run flash test
            Test_execResult,Test_executionEvalCount,Test_executionEvalFailed = exec_JNK_test.run_test(n_tests =TestList,n_rtests = Tests_run, testsetnumber = flash_test_idx, testName = flash_test_name.split('.')[0], projectPath = projectPath, seqPath = seqPath, cfgPath =cfgPath2, testPath = flash_test_path, repPath = repTestPath, repDirPath = repDirPath, log_file = exec_log_file) 
            #print("not flash")
            #print ('\nTM\nTM  Test Set Number ' +str(tst_idx) + ' finished.\n'+ 'TM      Test Execution Time: ' + str(t) + ' s\n'+'TM      Test Result: ' + str(Test_execResult) + 'TM      Number of executed tests: ' + str(tst_idx) + ' / ' + str(len(PathsList_run)) + '\nTM\n'+'TM-TM-TM-TM-TM-TM-TM-TM-TM-TM-TM-TM-TM-TM-TM-TM-TM-TM\n')

        except (NameError, ValueError), e:
            print '--> Exception !!!'
            print 'SW_Flash.xml is not available into tests folder. Consequently the SW flashing is not possbile'
        except :
            print 'Exception occurred during flashing process !!'
        t = int((time.clock() - t) * 100) / 100.0
        totalT += t
        #print(Test_execResult)
        # store test execution result 
        testResult = [flash_test_name.split('.')[0], Test_execResult, Test_executionEvalCount, Test_executionEvalFailed]
        execResults.append(testResult)
        print('\nTM\nTM  Test Set Number ' +str(flash_test_idx) + ' finished.\n' + 
                        'TM      Test Execution Time: ' + str(t) + ' s\n'
                        'TM      Test Result: ' + str(Test_execResult) + '\n' + 
                        'TM      Number of executed tests: ' + str(flash_test_idx) + ' / ' + str(len(PathsList_run)-1) + '\nTM\n' + 
                        'TM-TM-TM-TM-TM-TM-TM-TM-TM-TM-TM-TM-TM-TM-TM-TM-TM-TM\n')
        ################### END Flash new SW ####################### 
        
        ################### Execute Tests ####################### 
        tst_idx = 0
        tst_run_idx=len(PathsList_run)
        while (tst_idx < len(PathsList_run)):
            testName = TestsList[tst_idx]        
            testPath = r'%s' %(PathsList_run[tst_idx])  
            #print(testName)
            # configure test reporting paths
            repTestPath = repPath + '\\' +testName.split('.')[0] + '\\' + testName
            repDirPath = repPath + '\\' + testName.split('.')[0]
            t = time.clock()   
            # run test
            Test_execResult,Test_executionEvalCount,Test_executionEvalFailed = exec_JNK_test.run_test(n_tests =TestList, n_rtests = Tests_run,testsetnumber =tst_idx, testName = testName.split('.')[0], projectPath = projectPath, seqPath = seqPath, cfgPath =cfgPath, testPath = testPath, repPath = repTestPath, repDirPath = repDirPath, log_file = exec_log_file)        
            t = int((time.clock() - t) * 100) / 100.0
            totalT += t
            # store test execution result
            #print(Test_execResult)
            print('\nTM\nTM  Test Set Number ' +str(tst_idx) + ' finished.\n' + 
                        'TM      Test Execution Time: ' + str(t) + ' s\n'
                        'TM      Test Result: ' + str(Test_execResult) + '\n' + 
                        'TM      Number of executed tests: ' + str(tst_idx) + ' / ' + str(len(PathsList_run)-1) + '\nTM\n' + 
                        'TM-TM-TM-TM-TM-TM-TM-TM-TM-TM-TM-TM-TM-TM-TM-TM-TM-TM\n')
            testResult = [testName.split('.')[0], Test_execResult, Test_executionEvalCount, Test_executionEvalFailed]
            execResults.append(testResult)
            tst_idx += 1
        ################### END Execute Tests #######################     

        ################### Store Test execution results #######################
        #print("file")
        to_File = ''   
        for testResultElem in execResults:
            to_File += str(testResultElem[0]) + ' - ' + str(testResultElem[1]) + ' - ' + str(testResultElem[2]) + ' - ' + str(testResultElem[3]) + '\n'
        TestExecResult.write(to_File) # write tests execution results to file
        TestExecResult.close()
        ################### END Store Test execution results ####################### 
        # convert from sec in min and days
        totalT = int(totalT)
        #print("cal")
        totalTDays = divmod(totalT, 3600*24)[0]
        totalTHours = divmod(totalT, 3600)[0]
        totalTMins = divmod(totalT, 60)[0]
        totalTSecs = divmod(totalT, 60)[1]
        #############################################
        print(            
            'TM  Run finished.\n' + 
            'TM\n' + 
            'TM  Number of executed tests: ' + str(tst_idx) + ' / ' + str(len(PathsList_run)) + '\n'+
            'TM  Total execution time: ' + str(totalTDays) + 'd '
                                         + str(totalTHours) + 'h ' 
                                         + str(totalTMins) + 'm '
                                         + str(totalTSecs) + 's\n' +
            'TM\n' +
            'TM-TM-TM-TM-TM-TM-TM-TM-TM-TM-TM-TM-TM-TM-TM-TM-TM-TM\n')

        print ('End execution for all tests')
        exec_log_file.close()
    elif string == 'norun':
        print 'norun'
        print(" Project or cluster is not available ")
