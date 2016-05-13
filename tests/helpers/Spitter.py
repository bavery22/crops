#!/usr/bin/python
''' Run Cmd while keeping stdout active'''


import subprocess
import os.path
import glob
import argparse

import threading
import time

class SpitMsg(threading.Thread):
    def __init__(self,cmd,msg="Keep Travis Happy",timeout=60):
        threading.Thread.__init__(self)
        self.msg=msg
        self.cmd = cmd
        self.timeout=timeout
        self.keepGoing=True

    def run(self):
        while self.keepGoing:
            print(self.msg);
            time.sleep(self.timeout)
    def setTimeout(self,t):
        self.timeout=t
    def setMsg(self,m):
        self.msg=m
    def setKeepGoing(self,flag):
        self.keepGoing=flag
    def go(self):
        self.start()
        try:
            subprocess.call(self.cmd.split())
        except subprocess.CalledProcessError as e:
            print e.output
            self.assertTrue(False)
        self.keepGoing=False

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("--command", "-c", help="command to run"
                        "while chatty runs in background")
    parser.add_argument("--timeout", "-t", help="how often to"
                        "spit out msg")
    parser.add_argument("--message", "-m", help="Witty msg to spit")


    args = parser.parse_args()
    if args.command:
        mySpitter=SpitMsg(args.command)
        if args.message:
            mySpitter.setMsg(args.message)
        if args.timeout:
            mySpitter.setTimeout(float(args.timeout))
        mySpitter.go()
