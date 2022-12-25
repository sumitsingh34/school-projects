#!/usr/bin/env python3
import os
import sys
import re
import numpy as np
from random import choice, randrange, shuffle
from itertools import combinations, chain


def threeWordsShingles(file):      # returns a list of words from a file & being called in 'charfunc'

    if os.path.isfile(file):
        try:
            with open(file) as fd:
                s = fd.read()
        except:
            print(file,
                  ": Please provide a valid file location with name like: '/u1/class/cs61715/Project/Files/file0001' as file location!",
                  file=sys.stderr)
            sys.exit(0)
    else:
        print(file,
              ": Please provide a valid file location with name like: '/u1/class/cs61715/Project/Files/file0001' as file location!",
              file=sys.stderr)
        sys.exit(0)

    removePunctuation = s.translate({ord(c): "" for c in '!()[]{};:,./?\|-`”“’—"'}).lower()[:-1]
    removed = removePunctuation.replace("'",' ')
    r2 = removed.replace('  ','')
    s1 = r2.replace('\n',' ')
    s2 = s1.replace('\t','')
    s = re.sub(r'<.*>', "", s2)
    s1List = s.split(' ')

    return s1List



def charfunc(filename, sdict3index):

    if os.path.isfile(filename):
        try:
            with open(filename) as fd:
                s2 = fd.read()
        except:
            print(filename,
                  ": Please provide a valid file location with name like: '/u1/class/cs61715/Project/Files/file0001' as file location!",
                  file=sys.stderr)
            sys.exit(0)
    else:
        print(filename,
              ": Please provide a valid file location with name like: '/u1/class/cs61715/Project/Files/file0001' as file location!",
              file=sys.stderr)
        sys.exit(0)

    s1List = threeWordsShingles(filename)

    fileDict = { " ".join(s1List[i:i+3]) for i in range(len(s1List)-2) }

    size = len(sdict3index)
    fileArray = np.zeros(size, dtype=np.uint8)

    for k, i in sdict3index.items():
        if k in fileDict:
            fileArray[i] = 1

    return fileArray



def generate_primes(numofprime):   # used this prime generation code from class lecture
    mask = [0]*numofprime
    primelist = []
    for num in range(3,numofprime,2):
        if mask[num] != 0:
            continue
        primelist.append(num)
        for n in range(num,numofprime,2*num):
            mask[n] = 1
    return primelist



def generate_hashfuncs(num1,num2,div):
    def hfunc(mul):
        return (num1*mul+num2) % div
    return hfunc



def create_minhashList(atleast_how_many_shingles, numofrows, bigarray):

    barraysimi = bigarray[bigarray.sum(axis=1) >= atleast_how_many_shingles]
    barraysimiStackZeros = np.vstack([[0] * barraysimi.shape[1], barraysimi])

    primelist = generate_primes(barraysimiStackZeros.shape[0])
    num1list = [choice(primelist) for _ in range(numofrows)]
    num2list = [randrange(barraysimiStackZeros.shape[0]) for _ in range(numofrows)]
    hashfunclist = [generate_hashfuncs(num1list[i], num2list[i], barraysimiStackZeros.shape[0]) for i in
                    range(numofrows)]

    minhashvalues = []
    for hfunc in hashfunclist:
        minhash = [0] * barraysimiStackZeros.shape[1]
        # new_array = []
        for i in range(1, numofrows):
            hashval = hfunc(i)

            # new_array.append(barraysimiStackZeros[hashval])   # just for debugging

            onespositions = [x for x in range(barraysimiStackZeros.shape[1]) if barraysimiStackZeros[hashval, x] == 1]
            for pos in onespositions:
                if minhash[pos] == 0:
                    minhash[pos] = i

        minhashvalues.append(minhash)

    minhashlist = np.array(minhashvalues)

    return minhashlist



def create_doc_similarityGroup(minhashlist, num_of_rows_perblock):

    simil_docs_dict = [] # dict()

    for row in range(0, minhashlist.shape[0], num_of_rows_perblock):
        temp = dict()
        for col in range(minhashlist.shape[1]):
            colvalue = tuple(minhashlist[row:row + num_of_rows_perblock:, col])

            #fileNumber = col + 1
            #colvaluestr = " ".join(["".join(item) for item in colvalue.astype(str)])

            if colvalue == (0,)*num_of_rows_perblock: # skipping all zeros columns
                continue

            if colvalue in temp:
                prevValuesSet = temp.get(colvalue)
                if col not in prevValuesSet:
                    newValuesSet = prevValuesSet + [col]
                    temp.update({colvalue: newValuesSet})
            else:
                temp.update({colvalue: [col] })

        simil_docs_dict.append(temp)

    return simil_docs_dict


# started:: Prof. code to find connected components

# Find connected components of graph (input as edge list).
def read_elist(elist):
    global N

# find N, the order (number of vertices) of the graph
    N = max(chain(*elist)) + 1

# create the data structure used by the algorithm

    verts = [{'vis':False, 'scan':False, 'nbr':[]} for _ in range(N)]
    for u,v in elist:
        verts[u]['nbr'].append(v)
        verts[v]['nbr'].append(u)

# return the data structure

    return verts

def find_not_vis(verts):    # find an unvisited vertex
    global N

    for i in range(N):
        if not verts[i]['vis']:
            return i
    return None

def find_vis_not_scan(verts):  # find a visited but unscanned vertex
    global N

    for i in range(N):
        if verts[i]['vis'] and not verts[i]['scan']:
            return i
    return None

# end:: of prof. code to find connected components



if __name__ == "__main__":


    if len(sys.argv) != 2:
        print(f"To run {sys.argv[0]:s}, Please provide '/u1/class/cs61715/Project/Files' as an argument!", file=sys.stderr)
        sys.exit(0)

    sdict = {}
    allfilesdir = sys.argv[1]             # /u1/class/cs61715/Project/Files
    try:
        filelist = os.listdir(allfilesdir)
    except:
        print(allfilesdir,"Please provide '/u1/class/cs61715/Project/Files' as file directory!", file=sys.stderr)
        sys.exit(0)

    numofarticles = len(filelist)

    #preparing dictionary of shingles
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

    # taking only important shingles
    sdictatleast2 = { key:val for key,val in sdict.items() if val > 1 }

    sdict3index = { k:i for i, k in enumerate(sdictatleast2) }
    rows = len(sdict3index)

    print("Creating bigarray...\n")
    bigarray = np.arange(numofarticles * rows, dtype=np.uint8).reshape((rows, numofarticles))
    filelist.sort()                                         # sorted becuase name of file are coming randomly

    for index, articlename in enumerate(filelist):
        articlepath = allfilesdir + "/" + articlename
        if os.path.isfile(articlepath):
            fileArray = charfunc(articlepath, sdict3index)  # generating array for each file
            bigarray[:, index] = fileArray                  # creating big array returned after each file

    print("Bigarray has been created!\n")

    atleast_how_many_shingles = 15           # 5, 10, 15, 20, 25
    numofrows = 120                         # 24, 60, 120, 96, 144 or 156,
    num_of_rows_perblock = 4                 # 2, 3 or 4
    two_columns_minhash_match_count = 2      # 1 or 2

    print("Generating minhash list...\n")

    minhashlist = create_minhashList(atleast_how_many_shingles, numofrows, bigarray)
    simil_docs_dict = create_doc_similarityGroup(minhashlist, num_of_rows_perblock)

    print("Minhash list created successfully!\n")

    print("generating pairs of documents...\n")

    onlyMatchingPairsList = []
    for i in range(len(simil_docs_dict)):
        pairDict = {k: v for k, v in simil_docs_dict[i].items() if len(v) >= two_columns_minhash_match_count}
        onlyMatchingPairsList.append(pairDict)

    pair_doc_list = []
    print("Following are similar pairs of documents\n")
    for j in range(len(onlyMatchingPairsList)):
        for k, v in onlyMatchingPairsList[j].items():
            print([ filelist[index] for index in v ])
            print('==================================')
            for pair in combinations(v, 2):
                if pair not in pair_doc_list:
                    pair_doc_list.append(pair)

    print("pairs of documents created successfully....\n")

    print("Finding similar documents' groups...")

    verts = read_elist(pair_doc_list)

    groupNo = 1
    while (i := find_not_vis(verts)) != None:
        verts[i]['vis'] = True
        print(f"\nThe following documents are similar (Group Number: {groupNo}) :\n")
        groupNo += 1
        while (j := find_vis_not_scan(verts)) != None:
            verts[j]['scan'] = True
            print(filelist[j], end='  ')
            for k in verts[j]['nbr']:
                if not verts[k]['vis']:
                    verts[k]['vis'] = True
        print()
    print("\na) Pairs of documents & b) Similiar documents groups :: both has been printed on console!\n")
