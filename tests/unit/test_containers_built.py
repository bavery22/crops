#!/usr/bin/env python

import unittest
import os
import subprocess
import shutil
import tempfile
import sys
import stat
import imp


def checkPresent(myDict,myStream):
    for l in myStream:
        for k,v in  myDict.iteritems():
            repo=v['name'].split(':')[0]
            tag=v['name'].split(':')[1]
            if repo in l and tag in l :
                v['found']=True
    present=True
    for v in  myDict.itervalues():
        present &= v['found']
    return present

class TestContainersBuilt(unittest.TestCase):
    def setUp(self):
        self.sdkTargets = os.environ['TARGETS'].split()
        self.sdkYPRelease = os.environ['YP_RELEASE']
        self.zephyrRelease = os.environ['ZEPHYR_RELEASE']
        self.ostroRelease =  os.environ['OSTRO_RELEASE']
        self.sdkCropsRelease = os.environ['CROPS_RELEASE']
        self.dockerhubRepo = os.environ['DOCKERHUB_REPO']
        self.sdkD={}
        for t in self.sdkTargets:
            self.sdkD[t]={}
            self.sdkD[t]['name']="%s/toolchain-%s:%s"%(self.dockerhubRepo,t,self.sdkYPRelease)
            self.sdkD[t]['found']=False
        self.zephyrD={}
        self.zephyrD['i686']={}
        self.zephyrD['i686']['name']="%s/zephyr:%s"%(self.dockerhubRepo,self.zephyrRelease)
        self.zephyrD['i686']['found']=False

        self.ostroD={}
        self.ostroD['i686']={}
        self.ostroD['i686']['name']="%s/ostrobuilder:%s"%(self.dockerhubRepo,self.ostroRelease)
        self.ostroD['i686']['found']=False

    def tearDown(self):
        pass


    def test_sdk_containers_built(self):
        cmd = """docker  images """
        p=subprocess.Popen(cmd.split(), stderr=sys.stderr, stdout=subprocess.PIPE,
                        shell=False)

        allBuilt=checkPresent(self.sdkD,p.stdout)
        self.assertTrue(allBuilt)


    def test_zephyr_containers_built(self):
        cmd = """docker  images """
        p=subprocess.Popen(cmd.split(), stderr=sys.stderr, stdout=subprocess.PIPE,
                        shell=False)

        allBuilt=checkPresent(self.zephyrD,p.stdout)
        self.assertTrue(allBuilt)


    def test_ostro_containers_built(self):
        cmd = """docker  images """
        p=subprocess.Popen(cmd.split(), stderr=sys.stderr, stdout=subprocess.PIPE,
                        shell=False)

        allBuilt=checkPresent(self.ostroD,p.stdout)
        self.assertTrue(allBuilt)



if __name__ == '__main__':
    unittest.main()
