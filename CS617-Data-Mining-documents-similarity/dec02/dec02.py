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


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print(f"To run {sys.argv[0]:s}, Please provide '/u1/class/cs61715/Project/nov30/bigarray.npy' as argument!", file=sys.stderr)
        sys.exit(0)

    barrayfilename = sys.argv[1]              # bigarray.npy generated from nov18.py

    # loading the same bigarray file which generated from nov28.py
    if os.path.isfile(barrayfilename):
        try:
            bigarrayloaded = np.load(barrayfilename)
        except:
            print(barrayfilename,": Please provide a valid pickle file location like '/u1/class/cs61715/Project/nov30/bigarray.npy' ",  file=sys.stderr)
            sys.exit(0)
    else:
        print(barrayfilename,": Please provide a valid pickle file location like '/u1/class/cs61715/Project/nov30/bigarray.npy' ",  file=sys.stderr)
        sys.exit(0)
    #print(bigarrayloaded.shape) #(112727, 1277)
    #input()

    how_many_doc_simi = 4
    barraysimi = bigarrayloaded[bigarrayloaded.sum(axis=1) > how_many_doc_simi]

    barraysimiStackZeros = np.vstack([[0]*barraysimi.shape[1],barraysimi])
    #print(barraysimiStackZeros.shape)

    primelist = generate_primes(barraysimiStackZeros.shape[0])
    numofrows = 120 # 24, 60 or 120
    num1list = [choice(primelist) for _ in range(numofrows)]
    num2list = [randrange(barraysimiStackZeros.shape[0]) for _ in range(numofrows)]
    hashfunclist = [generate_hashfuncs(num1list[i],num2list[i],barraysimiStackZeros.shape[0]) for i in range(numofrows)]

    minhashvalues = []
    for hfunc in hashfunclist:
        minhash = [0]*barraysimiStackZeros.shape[1]
        new_array = []
        for i in range(1,numofrows):
            hashval = hfunc(i)

            new_array.append(barraysimiStackZeros[hashval])   # just for debugging

            onespositions = [x for x in range(barraysimiStackZeros.shape[1]) if barraysimiStackZeros[hashval, x] == 1]
            for pos in onespositions:
                if minhash[pos] == 0:
                    minhash[pos] = i

            #print(minhash)

        minhashvalues.append(minhash)

        # degugging started
        print('new_array is :')
        print(np.array(new_array))
        print('new array minhash values are:')
        print(np.array(minhash))

        #print(np.count_nonzero(minhash))
        print("\n above array's index starts with 1 because I'hv stacked the array with zeros")
        flag = input("Please Press Enter for more and '0' to exit: ")
        print(flag)
        if flag == '0':
            break

    # minhashlist = np.array(minhashvalues)
    # print('minhashlist', minhashlist)
