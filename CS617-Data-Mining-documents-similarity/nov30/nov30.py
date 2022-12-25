#!/usr/bin/env python3
import os
import sys
import numpy as np
import pickle
#import re
sys.path.insert(1, '/u1/class/cs61715/Project/nov29')
from nov29 import charfunc



if __name__ == "__main__":

    if len(sys.argv) != 3:
        print(f"To run {sys.argv[0]:s}, Please provide '/u1/class/cs61715/Files' '/u1/class/cs61715/Project/nov18/testpickle.pkl' as arguments!", file=sys.stderr)
        sys.exit(0)

    allfilesdir = sys.argv[1]             # /u1/class/cs61715/Files
    picklefile = sys.argv[2]              # testpcikle.pkl generated from nov18.py

    try:
        filelist = os.listdir(allfilesdir)
    except:
        print(allfilesdir,": Please provide '/u1/class/cs61715/Files' as file directory!",file=sys.stderr)
        sys.exit(0)

    numofarticles = len(filelist)

    # loading the same pickle file which generated from nov18.py
    try:
        with open(picklefile, 'rb') as fd:
            sdict3indexloaded = pickle.load(fd)
    except:
        print(picklefile,": Please provide a valid pickle file location like '/u1/class/cs61715/Project/nov18/testpickle.pkl' ", file=sys.stderr)
        sys.exit(0)

    # for unit testing
    #sdict3indexloaded.update({('a','b','c'):-1})
    #sdict3indexloaded.update({('a::b::c'): -1})

    rows = len(sdict3indexloaded)

    bigarray = np.arange(numofarticles * rows, dtype=np.uint8).reshape((rows, numofarticles))
    filelist.sort()   # sorted becuase name of file are coming randomly

    for index, articlename in enumerate(filelist):
        articlepath = allfilesdir + '/' + articlename
        if os.path.isfile(articlepath):
            a = charfunc(articlepath,sdict3indexloaded)                             #generating array for each file
            bigarray[:, index] = a                                      #creating big array returned after each file


    barrayfilename = 'bigarray.npy'
    np.save(barrayfilename,bigarray)
    print(f"'{barrayfilename}' has been generated in the current directory of shape {bigarray.shape}.")

    #checked whether the array before and after save is same or not
    #bigarrayloaded = np.load(barrayfilename)
    #print(np.sum(bigarrayloaded[:, 3]))
