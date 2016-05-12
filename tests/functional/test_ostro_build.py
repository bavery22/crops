''' Test Zephyr Build'''
import unittest
import re
import subprocess
import os.path
import utils.ceedutil as ceedutil
import glob

# This test set ASSUMES the initial scripts have been run and therefore we have
# 1) ostro container crops/ostrobuilder:v1.0.0
# 2) Currently assuming we are running on linix/Travis. We need docker-machine checks added to run on pc/mac as well.

def countRunTasks(d,v=False):
    fileList=glob.glob(d+'/*.log')
    if len(fileList) > 1:
        if v:
            for f in fileList:
                print ("Found too many files: %s\n"%f)
            return 100000
    # generate the list by whittling it down
    wSet=[ line for line in open(fileList[0]) if 'task' in line]
    wSet=[ line for line in wSet if 'do_compile'  in line]
    wSet=[ line for line in wSet if 'Running'  in line]
    if (v):
        for l in wSet:
            print("Run Entry->%s"%l.strip())

    return(len(wSet))



class OstroBuildTest(unittest.TestCase):
    ''' Base class for testing Ostro builds '''

    def setUp(self):
        ''' Define some unique data for validation '''
        # TODO:need to use a check for docker machine and get ip if pc/mac
        #self.dockerAddress = ceedutil.getDockerAddress().strip()
        self.makeScript='./scripts/bitbake.ostro'
        self.buildPath=os.environ['HOME']+"/ostro-workspace/"
        self.noswupdImage=self.buildPath+"/ostro-shared/images/intel-corei7-64/ostro-image-noswupd-intel-corei7-64.dsk"
        self.devnull=open(os.devnull, 'w')

    def tearDown(self):
        ''' Destroy unique data '''
        pass

    def test_noswupd_build(self):
        ''' Build ostro-image-noswupd\n'''
        TARGET="ostro-image-noswupd"
        try:
            os.mkdir(self.buildPath)
            subprocess.call([self.makeScript,TARGET],cwd=self.buildPath,stdout=self.devnull)
        except subprocess.CalledProcessError as e:
            print e.output
            self.assertTrue(False)

        success=False

        if os.path.isfile(self.noswupdImage):
            success=True

        self.assertTrue(success)




    def test_noswupd_sstate(self):
        ''' Build ostro-image-noswupd\n'''

        PATH=self.buildPath+"/ostro-shared/log/cooker/intel-corei7-64"
        NUM_OK_TO_BUILD=10
        # 2nd argument prints out bad sstate pkgs
        self.assertTrue(countRunTasks(PATH,True)<=NUM_OK_TO_BUILD)
