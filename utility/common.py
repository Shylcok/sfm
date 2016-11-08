# -*- coding: utf-8 -*-
'''
Created on 2016��4��5��

@author: 55Haitao
'''

import platform
from utility.singleTon import SingleTon
import datetime
import os
import shutil
import threading
import traceback
import sys
from decimal import Decimal
import string
import math


@SingleTon
class Common(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.__taskId = 0
        self.lock = threading.Lock()

    def createDir(self, dir):
        if not os.path.exists(dir):
            os.makedirs(dir)

    def isLinux(self):
        return 'Linux' in platform.system()

    def mergerFile(self, flist, desFile):
        ofile = open(desFile, 'w')
        for fr in flist:
            for txt in open(fr, 'r'):
                ofile.write(txt)

        ofile.close()

    def removeDir(self, path):
        if not os.path.exists(path):
            return
        else:
            shutil.rmtree(path)

    def checkDigitSame(self, d1, d2):
        from utility.logTool import HT_ERROR
        try:
            ret = Decimal(d1) - Decimal(d2)
            if ret < Decimal("1.1") and ret > Decimal("-1.1"):
                return True
            else:
                return False
        except Exception, e:
            HT_ERROR(e.message)
            return False

    def getTaskId(self):
        self.lock.acquire()
        self.__taskId = self.__taskId + 1
        self.lock.release()
        return self.__taskId

    def getFileCount(self, filePath):
        thefile = open(filePath, 'rb')
        count = 0
        while True:
            buffer = thefile.read(1024 * 8192)
            if not buffer:
                break
            count += buffer.count('\n')
        thefile.close()

        return count

    def get_last_n_lines(self, logfile, n):
        n = string.atoi(n)
        blk_size_max = 4096
        n_lines = []
        with open(logfile, 'rb') as fp:
            fp.seek(0, os.SEEK_END)
            cur_pos = fp.tell()
            while cur_pos > 0 and len(n_lines) < n:
                blk_size = min(blk_size_max, cur_pos)
                fp.seek(cur_pos - blk_size, os.SEEK_SET)
                blk_data = fp.read(blk_size)
                assert len(blk_data) == blk_size
                lines = blk_data.split('\n')

                # adjust cur_pos
                if len(lines) > 1 and len(lines[0]) > 0:
                    n_lines[0:0] = lines[1:]
                    cur_pos -= (blk_size - len(lines[0]))
                else:
                    n_lines[0:0] = lines
                    cur_pos -= blk_size

                fp.seek(cur_pos, os.SEEK_SET)

        if len(n_lines) > 0 and len(n_lines[-1]) == 0:
            del n_lines[-1]
        return n_lines[-n:]

    def pagination(self, total, page, count):
        return {'allpage': math.ceil(total/float(count)), 'page': page, 'count': total}