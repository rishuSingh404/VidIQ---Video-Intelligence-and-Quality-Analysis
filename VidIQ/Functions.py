# -*- coding: utf-8 -*-
"""
Created on Thu Dec 26 01:07:48 2019

@author: user
"""

import numpy as np
import cv2
import math

def YComponent(fileName, H, W, frameNumber):
    fp = open(fileName, 'rb')               # Open file in binary-reading mode
    frameSize = int(int(H)*int(W)*3/2)      # Set the size of one frame (YUV4:2:0) = 1920*1080*1.5
    fp.seek(frameNumber*frameSize, 0)       # Search the file from beginning(0), (1) from the End, to the N th Frame
    
    H2 = int(H)//2                          # Size of H for U or V
    W2 = int(W)//2

    Yt = np.zeros((H,W), np.uint8, 'C')     # Create a 1920*1080 Array (Data type: uint8 = 0 to 255) to store Y info
    Ut = np.zeros((H2,W2), np.uint8, 'C')
    Vt = np.zeros((H2,W2), np.uint8, 'C')

    for m in range(H):
        for n in range(W):
            Yt[m,n] = ord(fp.read(1))       # ord: Data-type form [,] to be 0-255
    
    for m in range(H2):
        for n in range(W2):
            Ut[m,n] = ord(fp.read(1))       # Mixed with U and V info

    for m in range(H2):
        for n in range(W2):
            Vt[m,n] = ord(fp.read(1))       # Mixed with U and V info

    Ut = np.repeat(np.repeat(Ut,2,0),2,1)    # Up-scale to be 1920*1080              
    Vt = np.repeat(np.repeat(Vt,2,0),2,1)

    fp.close()
    return(Yt,Ut,Vt)

def jerkiness(K, mi, td):
    j=K*mi*td
    return j

def blockshaped(arr, nrows, ncols):
    h, w = arr.shape
    return (arr.reshape(h//nrows, nrows, -1, ncols)
               .swapaxes(1,2)
               .reshape(-1, nrows, ncols))

def AvgPixelIntensity(arr):
    arr = np.array(arr)
    pixel_value = arr > 10
    if pixel_value.any():
        return arr[pixel_value].mean()
    else:
        return 0.
    
def LaplacianEdge(filename):
    # loading image
    img = cv2.imread(filename)
    # converting to gray scale
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # convolute with proper kernels
    laplacian = cv2.Laplacian(img,cv2.CV_8U)
    i = laplacian.flatten()
    avg=AvgPixelIntensity(laplacian)
    count=sum(float(num) > 10 for num in i)
    edge = int(avg * count)
    return edge
    
def sigmoid(x):
    return 1 / (1 + math.exp(-x))
    