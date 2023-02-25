#!/usr/bin/env python3

import sys
import numpy as np
from matplotlib import pyplot as plt
import gzip
import struct
from scipy.special import expit
from random import randrange

files = [
    "t10k-images-idx3-ubyte.gz",
    "train-images-idx3-ubyte.gz",
    "t10k-labels-idx1-ubyte.gz",
    "train-labels-idx1-ubyte.gz"
]

HIDDEN = 400


def read_files(labels_file_name, images_file_name):         # reading data and formatting into desired shape(60000, 784), etc.
    
    eoh = 16
    labelhdr = 8
    
    with gzip.open(labels_file_name, 'rb') as fdlabl:
        all_labels = fdlabl.read()

    with gzip.open(images_file_name, 'rb') as fdimg:
        all_images = fdimg.read()

    header_labl = struct.unpack('>ii', all_labels[:labelhdr])
    header_img = struct.unpack('>iiii', all_images[:eoh])

    imagesize = header_img[2]*header_img[3]
    
    labels = np.frombuffer(all_labels[labelhdr:], dtype=np.uint8)
    images = np.frombuffer(all_images[eoh:], dtype=np.uint8).reshape(len(labels), imagesize)

    return images, labels


X_train, y_train = read_files(files[3], files[1])  # reformatting train-images & train-labels
X_test, y_test = read_files(files[2], files[0])    # reformatting t10k-images & t10k-labels

# Preprocessing: reducing pixel values from [0, 255] to [0, 1]
X_train = X_train / 255.0
X_test = X_test / 255.0

# One-hot encoding of the labels
y_train = np.eye(10)[y_train]
y_test = np.eye(10)[y_test]

# Permute the training & test data 
for i in range(10):
    permuted = np.random.permutation(X_train.shape[0])
    X_train = X_train[permuted, :]
    y_train = y_train[permuted, :]

    permuted = np.random.permutation(X_test.shape[0])
    X_test = X_test[permuted, :]
    y_test = y_test[permuted, :]

with open('X_train.npy','wb') as fd:        # saving traing data
    np.save(fd, X_train)

with open('X_test.npy','wb') as fd:         # saving test data
    np.save(fd, X_test)


# Professor's Code from twolayers.py :: Done in class
def training_round(w1, w2, x, y, alpha):
    
    a1 = expit(w1 @ x)
    yhat = expit(w2 @ a1)

    predict = np.argmax(yhat)

    delta2 = yhat - y                  
    delta1 = w2.T @ delta2             

    dw2 = alpha * np.outer(delta2,a1)   
    dw1 = alpha * np.outer(delta1,x)    
    w1 -= dw1
    w2 -= dw2

    return predict


def testing_round(w1, w2, x, y, answer):

    a1 = expit(w1 @ x)
    yhat = expit(w2 @ a1)

    predict = np.argmax(yhat)

    return predict


def train():
    
    alpha = 0.1                                             
    w1 = np.random.randn(HIDDEN*784).reshape(HIDDEN,784)    
    w2 = np.random.randn(10*HIDDEN).reshape(10,HIDDEN)      

    reps  = 100000
    right =     0

    for i in range(reps):               # traing round
         
        pictno = randrange(60000)       
    
        x = X_train[pictno]
        y = y_train[pictno]
        digit = np.argmax(y)               
        
        predict = training_round(w1,w2,x,y, alpha)

        if predict == digit:
            right += 1
        alpha *= 0.9997
        if (i+1) % 1000 == 0:
            print(f'{right/(i+1):10.6f}')

    #print(f'{alpha:12.9f}')
    with open('weights1.npy','wb') as fd:
        np.save(fd, w1)
    
    with open('weights2.npy','wb') as fd:
        np.save(fd, w2)
    
    right = 0
    for i in range(10):                     # testing round
        for j in range(10000):
            x = X_test[j]
            y = y_test[j]
            digit = np.argmax(y)
            predict = testing_round(w1, w2, x, y, i)
            if predict == digit:
                right += 1

    print(right, 100000-right)
    print(f'Accuracy: {right/100000:10.6f}')


if __name__ == "__main__":

    train()