# -*- coding: utf-8 -*-
import os
import sys
import time
import logging

TEST_DIR = os.path.abspath(os.path.dirname(__file__))
PARENT_DIR = os.path.join(TEST_DIR, '..')
sys.path.insert(0, PARENT_DIR)

from zwutils.zwtask import ZWTask

if __name__ == '__main__':
    pypth, infos = ZWTask.stop_processes()
    print(pypth)
    for p in infos:
        print('%d %s'%(p['pid'], p['cmd']))