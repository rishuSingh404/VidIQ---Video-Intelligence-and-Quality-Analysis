# -*- coding: utf-8 -*-
"""
Created on Sat Dec  7 03:20:46 2019

@author: user
"""

# Get fps of a video:
# https://www.learnopencv.com/how-to-find-frame-rate-or-frames-per-second-fps-in-opencv-python-cpp/

# get timestamp of each frame in a video:
# https://stackoverflow.com/questions/47743246/getting-timestamp-of-each-frame-in-a-video
# https://stackoverflow.com/questions/51129425/how-to-get-frames-with-timestamp-where-frames-are-converted-from-video-in-python

# Y Componenet Extaction
# https://stackoverflow.com/questions/50888113/how-does-python-get-only-the-y-component-of-an-image

#filename = "video_bitstream/BigBuckBunny_SDH264HD_1.mp4"


import numpy as np
# import pandas as pd
import math
from Functions import YComponent
import openpyxl
from openpyxl.styles import Alignment

#image = Image.open('Frame\BBB\BBB_1\BBB_1_1.jpg')

Name = ['BigBuckBunny', 'BirdsInCage', 'BQTerrace', 'CrowdRun', 'DanceKiss', 'ElFuente1',
        'ElFuente2', 'FoxBird', 'Kimono1', 'OldTownCross', 'Seeking', 'Tennis']
FrameNo = [150, 180, 180, 150, 150, 180, 180, 150, 132, 150, 150, 120]
Format = ["_H264_","_SDH264HD_"]
File = ['BBB', 'BIC', 'BQT', 'CRN', 'DKS', 'EF1', 'EF2', 'FOX', 'KIM', 'OTC', 'SEE', 'TEN']

H=1080
W=1920

for vid in range(9,12):
    for f in range(0,2):
        for level in range(1,5):
            filename = 'Video/' + str(Name[vid]) + str(Format[f]) + str(level) + '.yuv'
            tempFileName =  str(Name[vid]) + str(Format[f]) + str(level)
            workbook_name = 'Jerkiness/'+ tempFileName + '_Jerkiness.xlsx'
            book = openpyxl.load_workbook(workbook_name)
            sheet = book.active
            sheet['C1']='Motion Intensity'
            sheet['C1'].alignment=Alignment(wrap_text=True)
            sheet['C2']=0
            
            for i in range(1,FrameNo[vid]):
                YComp1, u1, v1 = YComponent(filename,H,W,i-1)
                YComp1 = YComp1.astype(np.int64).flatten() 
                YComp2, u2, v2 = YComponent(filename,H,W,i)
                YComp2 = YComp2.astype(np.int64).flatten() 
                MotionIntensity = YComp2-YComp1
                MotionIntensity = pow(MotionIntensity,2)
                MotionIntensity = sum(MotionIntensity)
                MotionIntensity = math.sqrt(MotionIntensity)
                print(filename)
                print("Frame "+str(i)+": "+str(MotionIntensity))
                sheet['C'+str(i+2)]=MotionIntensity
                          
            book.save(workbook_name)
            print("\n")
    