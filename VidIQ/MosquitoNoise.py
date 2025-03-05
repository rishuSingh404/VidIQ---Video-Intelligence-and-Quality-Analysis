# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 18:51:27 2020

@author: user
"""

"""
References:
    https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_transforms/py_fourier_transform/py_fourier_transform.html
    https://akshaysin.github.io/fourier_transform.html#.XlyMk6gzZPY
    https://www.bogotobogo.com/python/OpenCV_Python/python_opencv3_Image_Gradient_Sobel_Laplacian_Derivatives_Edge_Detection.php
"""

import warnings
warnings.filterwarnings("ignore")
# import cv2
# import numpy as np
# from matplotlib import pyplot as plt
import openpyxl
# from openpyxl.styles import Alignment
from Functions import LaplacianEdge, sigmoid

Name = ['BigBuckBunny', 'BirdsInCage', 'BQTerrace', 'CrowdRun', 'DanceKiss', 'ElFuente1',
        'ElFuente2', 'FoxBird', 'Kimono1', 'OldTownCross', 'Seeking', 'Tennis']
FrameNo = [150, 180, 180, 150, 150, 180, 180, 150, 132, 150, 150, 120]
FileFormat = ["_H264_","_SDH264HD_"]
Format = ["","N"]
File = ['BBB', 'BIC', 'BQT', 'CRN', 'DKS', 'EF1', 'EF2', 'FOX', 'KIM', 'OTC', 'SEE', 'TEN']

for vid in range(0,12):
    for f in range(0,2):
        for level in range(1,5):
            book = openpyxl.Workbook()
            sheet = book.active
            sheet['A1'] = 'Frame'
            sheet['B1'] = 'EdgePixelIntensityDiff'
            sheet['C1'] = 'EdgePixelIntensityDiff(Scaled)'
            sheet['D1'] = 'MosquitoNoise'
            sheet['A2'] = 1
            sheet['B2'] = 0
            sheet['C2'] = 0
            sheet['D2'] = 0
            print('Extracting Mosquito Noise of ' + File[vid] + '_' + Format[f]  + str(level) + ', frame ' + str(1))
            print('Pixel Intensity Difference of Edge: ' + str(0))
            for frame in range(2, FrameNo[vid] + 1):
                print('Extracting Mosquito Noise of ' + File[vid] + '_' + Format[f] + str(level) + ', frame ' + str(frame))
                filename1 = 'Frame/' + str(File[vid]) + '/' + File[vid] + '_' + str(Format[f]) + str(level) + '/' + File[vid] + '_' + str(Format[f]) + str(level) + '_' + str(frame-1) + '.jpg'
                filename2 = 'Frame/' + str(File[vid]) + '/' + File[vid] + '_' + str(Format[f]) + str(level) + '/' + File[vid] + '_' + str(Format[f]) + str(level) + '_' + str(frame) + '.jpg'
                
                # Calculate the Difference of the Pixel Intensity of Edge
                x1 = LaplacianEdge(filename1)
                x2 = LaplacianEdge(filename2)
                diff = abs(x2 - x1)
                
                # Algorithm = 1 - sigmoid(K * diff) 
                sheet['A'+str(frame + 1)] = frame
                sheet['B'+str(frame + 1)] = diff
                sheet['C'+str(frame + 1)] = diff * 0.000001
                sheet['D'+str(frame + 1)] = 1 - sigmoid(diff * 0.000001) 
                print('Pixel Intensity Difference of Edge: ' + str(diff) + ', Mosquito Noise: ' + str(1 - sigmoid(diff * 0.000001)))
            book.save('MosquitoNoise/' + str(Name[vid]) + FileFormat[f] + str(level) + '_MosquitoNoise.xlsx')
            print("\n")
                

