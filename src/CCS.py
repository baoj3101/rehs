#!/usr/bin/python3

'''
Parse sparse matrix from data file
'''
import re
import argparse

#=================================================================================
# Utility functions
#=================================================================================
def debug(matrix):
    for col in matrix:
        for cell in col:
            print (cell[0], cell[1], cell[2])    

def splitLine (line):
    toks = line.split(' ')
    return [int(toks[0]), int(toks[1]), float(toks[2])]

#=================================================================================
# Read input data from file
#=================================================================================
def readInput(in_file):
    fh = open (in_file)
    # get 1st line matrix size
    M = 0
    for line in fh:
        # skip comments
        if re.match("\%", line):
            continue
    
        if M == 0:                                   # 1st line of data size M N TOTAL
            cell = splitLine(line)
            M = cell[1]
            matrix = [[] for i in range(M + 1)]      # *** index starts from 1
            break

    # read data from file
    for line in fh:
        cell = splitLine(line)
        i = cell[0]
        j = cell[1]
        matrix[j].append(cell)                      # *** add to column MATRIX[j]
        if i > j:
            matrix[i].append([j, i, cell[2]])       # *** add symmetric value if not i == j
    
    fh.close()
    return matrix

#=================================================================================
# Put data into VAL/ROW/PTR
#=================================================================================
def storeData(matrix, out_file):
    VAL = []
    ROW = []
    PTR = [0]*len(matrix)
    PTR[0] = 1

    for col in matrix:                              # col is a list of one matrix column non-zero data
        for cell in col:
            i = cell[0]
            j = cell[1]
            VAL.append(cell[2])                     # put data into VAL/ROW/PTR
            ROW.append(i)
            PTR[j] += 1
            
    # process PTR
    for i in range(2, len(PTR)):
        PTR[i] += PTR[i-1]

    # output
    import sys
    with open(out_file, 'w') as fh:
        sys.stdout = fh
        print ("%BEGIN VAL", len(VAL))
        for val in VAL:
            print (val)
        print ("%BEGIN ROW", len(ROW))
        for val in ROW:
            print (val)
        print ("%BEGIN PTR", len(PTR))
        for val in PTR:
            print (val)
            
#=================================================================================
# Main
#=================================================================================
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Sparse Matrix Parser')
    parser.add_argument('--input', type=str, help='input data file')
    args = parser.parse_args()
  
    matrix = readInput(args.input)
    debug(matrix)
    storeData(matrix, args.input + ".out")
