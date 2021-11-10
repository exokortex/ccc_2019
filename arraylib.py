#!/usr/bin/env python3

import sys
import numpy as np
import math
import types




def treeLen(tree):
    lensum = 0
    if hasattr(tree, '__iter__'):
        for e in tree:
            lensum += treeLen(e)
    else:
        lensum += 1

    return lensum


def destructureList(ls, fmt):
    output = []
    stride = treeLen(fmt)
    e_offset = 0
    for i in range(len(fmt)):
        e_len = treeLen(fmt[i])
        output.append([ls[offs + e_offset:offs + e_offset + e_len] for offs in range(0, len(ls), stride)])
        e_offset += e_len

    return output

def readArray(inputfile, arrayformat=[int]):
    arrays = [None]*len(arrayformat)
    #print(arrays)
    with open(inputfile) as f:
        lines = f.readlines()
        dimensions = [int(x) for x in lines[0].strip().split()]
        for line in [l.strip().split() for l in lines[1:]]:
            for afi in range(len(arrayformat)):
                subarray_line = [arrayformat[afi](element) for element in line[afi::len(arrayformat)]]
                #print(afi, line, subarray_line)
                #print(afi, arrays)
                if arrays[afi] == None:
                    arrays[afi]= subarray_line
                else:
                    arrays[afi].append(subarray_line)


    return dimensions, arrays

if __name__ == "__main__":
    dim, arr = readArray(sys.argv[1], [int, int])
    print(dim, arr)


