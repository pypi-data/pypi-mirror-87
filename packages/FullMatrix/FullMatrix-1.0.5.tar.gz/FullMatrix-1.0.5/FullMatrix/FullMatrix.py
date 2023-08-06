#!/usr/bin/env python

import numpy as np
import pandas as pd
import os
import sys, getopt
import os.path
import argparse

dir = os.path.dirname(__file__)
version_py = os.path.join(dir, "_version.py")
exec(open(version_py).read())

def annotation(chrsize,index,output_file):
    result = pd.DataFrame()
    chrsize = int(chrsize)
    index = int(index)
    start = range(0,(chrsize-index),index)
    #end = range(index,chrsize,index)
    for i in start:
        df = pd.DataFrame()
        df = pd.DataFrame({'start1': i, 'start2': start})
        result = pd.concat([result, df])
    result.to_csv(output_file, sep='\t', index=False)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', dest='input',
                        required=True,
                        help='chromosome size(bp)')
    parser.add_argument('-r', '--resolution', dest='resolution',
                        required=True,
                        help='window size splitting chromosome')
    parser.add_argument('-o', '--output', dest='output',
                        default='full_matrix.bed',
                        help='Output file. [default: full_matrix.bed]')
    parser.add_argument("-V", "--version", action="version",version="FullMatrix {}".format(__version__)\
                      ,help="Print version and exit")
    args = parser.parse_args()
    print('###Parameters:')
    print(args)
    print('###Parameters')
    annotation(args.input,args.resolution,args.output)

if __name__ == '__main__':
    main()