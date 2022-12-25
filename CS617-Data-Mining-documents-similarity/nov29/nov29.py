#!/usr/bin/env python3
import os
import sys
import numpy as np
import pickle
import re
from itertools import combinations


def charfunc(filename, sdict3indexloaded):

    if (type(sdict3indexloaded) is dict):
        for keys in sdict3indexloaded.keys():
            if type(keys) is str:
                if " " not in keys:
                    print("please provide dictionary's keys as a string with spaces!!", file=sys.stderr)
                    sys.exit(0) #return None
            else:
                print("Dictionary key is not in string formate, please provide dictionary's keys as a string with spaces", file=sys.stderr)
                sys.exit(0) #return None
    else:
        print("Please provide a dictionary data type as a second argument", file=sys.stderr)
        sys.exit(0) #return None


    if os.path.isfile(filename):
        try:
            with open(filename) as fd:
                s2 = fd.read()
        except:
            print(filename,
                  ": Please provide a valid file location with name like: '/u1/class/cs61715/Files/file0001' as file location!",
                  file=sys.stderr)
            sys.exit(0) #return None
    else:
        print(filename,
              ": Please provide a valid file location with name like: '/u1/class/cs61715/Files/file0001' as file location!",
              file=sys.stderr)
        sys.exit(0) #return None

    removePunctuation2 = s2.translate({ord(c): "" for c in '!()[]{};:,./?\|-`”“’—"'}).lower()[:-1]
    removed2 = removePunctuation2.replace("'",' ')
    r3 = removed2.replace('  ','')
    sf = r3.replace('\n',' ')
    sfremoved = sf.replace('\t','')
    s = re.sub(r'<.*>', "", sfremoved)
    s2List = s.split(' ')

    fileDict = { " ".join(s2List[i:i+3]) for i in range(len(s2List)-2) }
    #print(fileDict)

    size = len(sdict3indexloaded)
    fileArray = np.zeros(size, dtype=np.uint8)

    for k, i in sdict3indexloaded.items():
        if k in fileDict:
            fileArray[i] = 1

    return fileArray



if __name__ == "__main__":

    if len(sys.argv) != 3:
        print(f"To run {sys.argv[0]:s}, Please provide '/u1/class/cs61715/Files/fileXXXX' '/u1/class/cs61715/Project/nov18/testpickle.pkl' as arguments!", file=sys.stderr)
        sys.exit(0)

    articlepath = sys.argv[1]             # e.g /u1/class/cs61715/Files/file0001
    picklefile = sys.argv[2]              # e.g testpcikle.pkl generated from nov18.py

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

    if os.path.isfile(articlepath):
        fileArray = charfunc(articlepath, sdict3indexloaded)  # generating array for individual file
        if fileArray is not None:
            print(f"{articlepath} file's array has been returned successfully!")
    else:
        print(articlepath,": Please provide a valid file location with name like: '/u1/class/cs61715/Files/file0001' as file location!", file=sys.stderr)
        sys.exit(0)

    #print(np.sum(fileArray))
    #print(fileArray)
