''' Test Zephyr Build'''
import unittest
import re
import subprocess
import os.path
import glob

# This test set ASSUMES the initial scripts have been run and therefore we have
# 1) ostro container crops/ostrobuilder:v1.0.0
# 2) Currently assuming we are running on linix/Travis. We need docker-machine checks added to run on pc/mac as well.

def countRunTasks(d,v=False):
    ''' counts number of non sstate tasks in collection of cooker logs'''
    fileList=glob.glob(d+'/*.log')
    n=0
    if len(fileList) == 0:
        if v:
            print ("No log file found!\n")
        return 100000
    # generate the list by whittling it down
    for f in fileList:
        wSet=[ line for line in open(f) if 'task' in line]
        wSet=[ line for line in wSet if 'do_compile'  in line]
        wSet=[ line for line in wSet if 'Running'  in line]
        if (v):
            for l in wSet:
                print("Run Entry->%s"%l.strip())
        n += len(wSet)
    return(len(wSet))

import threading
import time
class SpitMsg(threading.Thread):
    def __init__(self,msg,timeout):
        threading.Thread.__init__(self)
        self.msg=msg
        self.timeout=timeout
        self.keepGoing=True
    def run(self):
        while self.keepGoing:
            print(self.msg);
            time.sleep(self.timeout)
    def setKeepGoing(self,flag):
        self.keepGoing=flag


class OstroBuildTest(unittest.TestCase):
    ''' Base class for testing Ostro builds '''

    def setUp(self):
        ''' Define some unique data for validation '''
        # TODO:need to use a check for docker machine and get ip if pc/mac
        #self.dockerAddress = ceedutil.getDockerAddress().strip()
        self.noswupdImage="ostro-shared/images/intel-corei7-64/ostro-image-noswupd-intel-corei7-64.dsk"
        self.devnull=open(os.devnull, 'w')
        self.mySpitter=SpitMsg("Keeping Travis Timeouts Happy\n",1*60)
        self.mySpitter.start()

    def tearDown(self):
        ''' Destroy unique data '''
        self.mySpitter.setKeepGoing(False)


    def test_noswupd_build(self):
        ''' Check an ostro build of an ostro-image-noswupd'''
        ''' Assumes the build is completed elsewhere.  It '''
        ''' was broken up due to travis timeout issues when'''
        ''' we did a full build'''

        success=False

        if os.path.isfile(self.noswupdImage):
            success=True
        else:
            print("No Image File Found\n")
        # and check to see if we have an ok (0 is gr8)
        # number of sstate misses
        PATH="ostro-shared/log/cooker/intel-corei7-64"
        NUM_OK_TO_BUILD=10
        # 2nd argument prints out bad sstate pkgs
        n = countRunTasks(PATH,True)
        success |= n<=NUM_OK_TO_BUILD

        self.assertTrue(success)
