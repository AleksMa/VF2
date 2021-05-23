#!/usr/bin/env python3
import os
import sys
import time
from vf import Vf

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("sys.argv[1]: Graph file")
        print("sys.argv[2]: subGraph file")
        print("sys.argv[3]: output file")
        exit()
    
    start = time.time()    
    # output = open(sys.argv[3], 'w+')
    # sys.stdout = output
    
    vf2 = Vf()   
    res = vf2.main(sys.argv[1], sys.argv[2])   
    print(res)  

    end = time.time()
    # print "time: ", (end - start)/60
    # output.close()
