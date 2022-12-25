#!/usr/bin/env python3
import os
import sys
import numpy as np
import pickle
import re



def threeWordsShingles(file):

    with open(file) as fd:
        s = fd.read()

    removePunctuation = s.translate({ord(c): "" for c in '!()[]{};:,./?\|-`”“’—"'}).lower()
    removed = removePunctuation.replace("'",' ')
    r2 = removed.replace('  ','')
    s1 = r2.replace('\n','')
    s2 = s1.replace('\t','')
    s = re.sub(r'<.*>', "", s2)
    s1List = s.split(' ')


    return s1List



if __name__ == "__main__":

    if len(sys.argv) != 3:
        print(f"To run {sys.argv[0]:s}, Please provide '/u1/class/cs61715/Files' '<desired-output-file-name-without-extension>' as arguments!", file=sys.stderr)
        sys.exit(0)

    sdict = {}
    allfilesdir = sys.argv[1]             # /u1/class/cs61715/Files
    picklefilename = sys.argv[2] + '.pkl'  # shingles.pkl or anything else

    try:
        filelist = os.listdir(allfilesdir)
    except:
        print(allfilesdir,"Please provide '/u1/class/cs61715/Files' as file directory!")
        sys.exit()

    numofarticles = len(filelist)
    #print('numofarticles', numofarticles)

    for filename in filelist:
        filepath = allfilesdir + '/' + filename
        if os.path.isfile(filepath):
            s1List = threeWordsShingles(filepath)
            for i in range(len(s1List) - 2):
                shingle = " ".join(s1List[i:i + 3])
                if shingle in sdict:
                    sdict.update({shingle: sdict[shingle] + 1})
                else:
                    sdict.update({shingle: 1})

    #print(len(sdict))

    sdictatleast2 = { key:val for key,val in sdict.items() if val > 1 }
    #print(list(sdictatleast2.items())[-1])
    #print(len(sdictatleast2))

    sdict3index = { k:i for i, k in enumerate(sdictatleast2) }

    with open(picklefilename, 'wb') as fd:
        pickle.dump(sdict3index, fd, protocol=pickle.HIGHEST_PROTOCOL)
        print(f'{picklefilename} file has been generated in the current directory!!')

    # loaded the same pickle file and checked whether they are same or not.

    #with open(picklefilename, 'rb') as fd:
    #    sdict3indexloaded = pickle.load(fd)

    #print(sdict3index == sdict3indexloaded)
    #print(len(sdict3indexloaded))
