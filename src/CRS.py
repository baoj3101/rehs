#!/usr/bin/python3

import re

fn = './bcsstk15/bcsstk15.mtx'

in_fh = open(fn, 'r')
out_fh = open('log', 'w')

M = 0
N = 0
NUM = 0
VAL = []
COL = []
PTR = []
p = 0
tmp = []

for line in in_fh:
    line = line.strip()
    if re.match("^\%", line):
        continue
    
    if NUM == 0:
        toks = line.split(' ')
        M = int(toks[0])
        N = int(toks[1])
        NUM = int(toks[2])
        
    else:
        toks = line.split(' ')
        i = int(toks[0])
        j = int(toks[1])
        #print("[" + line + "]\n")
        VAL.append(int(toks[2]))
        p+=1
        COL.append(j)
        if i in tmp:
            continue
        else:
            PTR.append(p)
            tmp.append(i)
                        
in_fh.close()
out_fh.close()
