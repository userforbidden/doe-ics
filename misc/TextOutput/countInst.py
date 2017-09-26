import re
import os, fnmatch
import glob
import shutil
import sys
import re
from collections import Counter

numOfInst = 60

class Inst:
    def __init__(self):
        self.XIC=(0, "XIC")
        self.XIO=(1, "XIO")
        self.OTE=(2, "OTE")
        self.OTL=(3, "OTL")
        self.OUT=(4, "OUT")
        self.OSR=(5, "OSR")
        self.TON=(6, "TON")
        self.TOF=(7, "TOF")
        self.RTO=(8, "RTO")
        self.CTU=(9, "CTU")
        self.CTD=(10, "CTD")
        self.RES=(11, "RES")
        self.JSR=(12, "JSR")
        self.SBR=(13, "SBR")
        self.RET=(14, "RET")
        self.JMP=(15, "JMP")
        self.LBL=(16, "LBL")
        self.MCR=(17, "MCR")
        self.TND=(18, "TND")
        self.EQU=(19, "EQU")
        self.GEQ=(20, "GEQ")
        self.GRT=(21, "GRT")
        self.LEQ=(22, "LEQ")
        self.LES=(23, "LES")
        self.LIM=(24, "LIM")
        self.MEQ=(25, "MEQ")
        self.NEQ=(26, "NEQ")
        self.ADD=(27, "ADD")
        self.SUB=(28, "SUM")
        self.MUL=(29, "MUL")
        self.DIV=(30, "DIV")
        self.SQR=(31, "SQR")
        self.NEG=(32, "NEG")
        self.ABS=(33, "ABS")
        self.TOD=(34, "TOD")
        self.FRD=(35, "FRD")
        self.DEG=(36, "DEG")
        self.RAD=(37, "RAD")
        self.SIN=(38, "SIN")
        self.COS=(39, "COS")
        self.TAN=(40, "TAN")
        self.ASN=(41, "ASN")
        self.ACS=(42, "ACS")
        self.ATN=(43, "ATN")
        self.LN=(44, "LN")
        self.LOG=(45, "LOG")
        self.XPY=(46, "XPY")
        self.MOV=(47, "MOV")
        self.MM=(48, "MM")
        self.CLR=(49, "CLR")
        self.SWPB=(50, "SWPB")
        self.SWP=(51, "SWP")
        self.AND=(52, "AND")
        self.OR=(53, "OR")
        self.XOR=(54, "XOR")
        self.NOT=(55, "NOT")
        self.SQO=(56, "DQO")
        self.SQL=(57, "SQL")
        self.SQC=(58, "SQC")
        self.END=(59, "END")


inst = Inst()

class merge():
    k = []

    def __init__(self):
        self.counter = [0] * numOfInst
        pass

    def oper(self, mylist):
        self.counter = [0] * numOfInst
        nlist = mylist[0]
        j = len(nlist)
        sym_list = []
        inst_list = []
        for i in range(0, j):
            x = nlist[i]
            s = x[x.find("[") + 1:x.find("]")]  # item between the square brackets
            inst_list.append(s)  # this list is for instructions to be printed
            if x.startswith('('):
                sym_list.append(x[1:4])  # extracting symbols like XIC and XIO
            else:
                sym_list.append(x[0:3])  # everything else like OTE,AND,OR,TON

        # nsym_list = sym_list.pop(0)					#removal of the first element 'rung'
        s_list = sym_list
        s_list = list(filter(None, s_list))

        for s in s_list:
            if s == '-->' or s=='Run':
                s_list.remove(s)
        # print s_list
        self.appendL(s_list)

    def appendL(self, mlist):
        self.k = self.k + mlist

    # print "Added",self.k


    def countM(self):
        print("from count", self.k)
        a = dict(Counter(self.k))
        print("Look at this", a)

    def countL(self):
        for i in self.k:
            for attr, value in inst.__dict__.items():
                if i == value[1]:
                    self.counter[value[0]] += 1

def main():
#    m = merge()
#    arg = sys.argv[1]

    print(",", end='')
    for i in range(len(merge().counter)):
        for attr, value in inst.__dict__.items():
            if i == value[0]:
                print(value[1]+",", end='')
    print("")

    for filename in os.listdir(os.getcwd() + "/txt/"):
        if filename.split(".")[-1] == "txt":
            filepath = os.getcwd() + "/txt/" + filename
            z = open(filepath, 'r+')
            linelist = []
            for word in z.readlines():  # listing the lines of text file
                line = [x.strip() for x in word.split(" ") if x != '']
                linelist.append(line)
            j = len(linelist)
            # print "line list", linelist

            # print "value of j is",j

            m = merge()
            for i in range(0, j):
                mylist = [linelist[i]]  # accessing line by line

                m.oper(mylist)
        #    m.countM()
            m.countL()

            print(filename[:-4] + ",", end='')
            for i in m.counter:
                print(i, ",", end='')
            print("")

if __name__ == '__main__':
    main()
