#!/usr/bin/env python3
import os
import sys

import numpy as np
from random import choice, randrange, shuffle
from itertools import combinations


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


def create_minhashList(atleast_how_many_shingles, numofrows, bigarrayloaded):

    barraysimi = bigarrayloaded[bigarrayloaded.sum(axis=1) >= atleast_how_many_shingles]
    barraysimiStackZeros = np.vstack([[0] * barraysimi.shape[1], barraysimi])
    #print(barraysimiStackZeros.shape)

    primelist = generate_primes(barraysimiStackZeros.shape[0])
    num1list = [choice(primelist) for _ in range(numofrows)]
    num2list = [randrange(barraysimiStackZeros.shape[0]) for _ in range(numofrows)]
    hashfunclist = [generate_hashfuncs(num1list[i], num2list[i], barraysimiStackZeros.shape[0]) for i in
                    range(numofrows)]

    arbitaryrange = 350
    minhashvalues = []
    for hfunc in hashfunclist:
        minhash = [0] * barraysimiStackZeros.shape[1]
        # new_array = []
        for i in range(1, arbitaryrange):
            hashval = hfunc(i)

            # new_array.append(barraysimiStackZeros[hashval])   # just for debugging

            onespositions = [x for x in range(barraysimiStackZeros.shape[1]) if barraysimiStackZeros[hashval, x] == 1]
            for pos in onespositions:
                if minhash[pos] == 0:
                    minhash[pos] = i

            # print(minhash)

        minhashvalues.append(minhash)

    minhashlist = np.array(minhashvalues)

    return minhashlist


def create_doc_similarityGroup(minhashlist, num_of_rows_perblock):

    simil_docs_dict = dict()

    for row in range(0, minhashlist.shape[0], num_of_rows_perblock):
        for col in range(minhashlist.shape[1]):
            colvalue = tuple(minhashlist[row:row + num_of_rows_perblock:, col])

            #fileNumber = col + 1
            #colvaluestr = " ".join(["".join(item) for item in colvalue.astype(str)])

            if colvalue == (0,)*num_of_rows_perblock: # skipping all zeros columns
                continue

            if colvalue in simil_docs_dict:
                prevValuesSet = simil_docs_dict.get(colvalue)
                if col not in prevValuesSet:
                    newValuesSet = prevValuesSet + [col]
                    simil_docs_dict.update({colvalue: newValuesSet})
            else:
                simil_docs_dict.update({colvalue: [col] })

    return simil_docs_dict



if __name__ == "__main__":

    if len(sys.argv) != 2:
        print(f"To run {sys.argv[0]:s}, Please provide '/u1/class/cs61715/Project/nov30/bigarray.npy' as argument!", file=sys.stderr)
        sys.exit(0)

    barrayfilename = sys.argv[1]              # bigarray.npy generated from nov30.py

    # loading the same bigarray file which generated from nov30.py
    if os.path.isfile(barrayfilename):
        try:
            bigarrayloaded = np.load(barrayfilename)
        except:
            print(barrayfilename,": Please provide a valid pickle file location like '/u1/class/cs61715/Project/nov30/bigarray.npy' ",  file=sys.stderr)
            sys.exit(0)
    else:
        print(barrayfilename,": Please provide a valid pickle file location like '/u1/class/cs61715/Project/nov30/bigarray.npy' ",  file=sys.stderr)
        sys.exit(0)

    atleast_how_many_shingles = 20 # 5, 10, 15, 20, 25
    numofrows = 156  # 24, 60, 120, 96, 144 or 156,
    num_of_rows_perblock = 4 # 2, 3 or 4
    two_columns_minhash_match_count = 2 # 1 or 2


    minhashlist = create_minhashList(atleast_how_many_shingles, numofrows, bigarrayloaded)
    #print('minhashlist', minhashlist.shape)
    simil_docs_dict = create_doc_similarityGroup(minhashlist, num_of_rows_perblock)
    #print('simil_docs_dict len',len(simil_docs_dict))

    onlyMatchingPairs = {k: v for k, v in simil_docs_dict.items() if len(v) >= two_columns_minhash_match_count}
    #print('onlyMatchingPairs len',len(onlyMatchingPairs))

    pair_doc_list = []
    for k,v in onlyMatchingPairs.items():
        for pair in combinations(v,2):
            if pair not in pair_doc_list:
                pair_doc_list.append(pair)
        print(f"Group = {k} & similar file list (pls add 1 if file sequence does not start with 0) = {v}")
        input('Please enter to get more...')

    #print("pairs of documents are:\n",pair_doc_list)
