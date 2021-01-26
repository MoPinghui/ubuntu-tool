
import os
import sys
import json
import numpy as np


class FD():
    def __init__(self):
        pass


    def get_all_file(self, sdir):
        dirList=os.listdir(sdir)
        dirList = [sdir + '/' + dire for dire in dirList]
        ext_dirList = []
        rm_dirList = []
        for dire in dirList:
            if os.path.isdir(dire):
                sub_dirList = self.get_all_file(dire)
                ext_dirList.extend(sub_dirList)
                rm_dirList.append(dire)
        dirList.extend(ext_dirList)
        for dire in rm_dirList:
            dirList.remove(dire)
        return dirList

    def find(self, sdir, mark):
        dirList = self.get_all_file(sdir)
        s2 = dirList
        for mark in marks:
            s1 = s2
            s2 = []
            for dire in s1:
                if mark in dire:
                    s2.append(dire)
        return s2

    def findd(self, sdir, mark):
        dirList = self.get_all_file(sdir)
        s2 = dirList
        for mark in marks:
            s1 = s2
            s2 = []
            for dire in s1:
                if mark in dire:
                    s2.append(dire)
        s1 = s2
        s2 = []
        for dire in s1:
            dire2 = dire.split('/')
            dire2 = '/'.join(dire2[:-1])
            if dire2 not in s2:
                s2.append(dire2)
        return s2
    
    def display_dirList(self, dirList):
        for dire in dirList:
            print(dire)


# -- mian --
if (__name__ == "__main__"):
    argvs = sys.argv[1:]
    if len(argvs) == 0:
        argvs = ['-h']
    
    fdObj = FD()
    if argvs[0] in ['find']:
        if len(argvs) == 1: print("please input a path")
        if len(argvs) == 2:
            dire = argvs[1]
            dirList = fdObj.get_all_file(dire)
            fdObj.display_dirList(dirList)
        if len(argvs) >= 3:
            dire = argvs[1]
            marks = argvs[2:]
            dirList = fdObj.find(dire, marks)
            fdObj.display_dirList(dirList)
    if argvs[0] in ['findd']:
        if len(argvs) == 1: print("please input a path")
        if len(argvs) >= 3:
            dire = argvs[1]
            marks = argvs[2:]
            dirList = fdObj.findd(dire, marks)
            fdObj.display_dirList(dirList)
    if argvs[0] == '-h' or argvs[0] == '--help':
        print("find: find the file in the directory.")