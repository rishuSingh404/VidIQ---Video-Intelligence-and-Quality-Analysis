# -*- coding: utf-8 -*-
"""
Created on Mon Dec 23 22:49:12 2019

@author: user
"""

import numpy as np
from Functions import YComponent, blockshaped
import openpyxl
from openpyxl.styles import Alignment

# filename = "Video/BigBuckBunny_H264_1.yuv"
#image = Image.open('Frame\BBB\BBB_1\BBB_1_1.jpg')

Name = ['BigBuckBunny', 'BirdsInCage', 'BQTerrace', 'CrowdRun', 'DanceKiss', 'ElFuente1',
        'ElFuente2', 'FoxBird', 'Kimono1', 'OldTownCross', 'Seeking', 'Tennis']
FrameNo = [150, 180, 180, 150, 150, 180, 180, 150, 132, 150, 150, 120]
Format = ["_H264_","_SDH264HD_"]
File = ['BBB', 'BIC', 'BQT', 'CRN', 'DKS', 'EF1', 'EF2', 'FOX', 'KIM', 'OTC', 'SEE', 'TEN']

H=1080
W=1920
threshold=300
h=8
w=16
noOfBlocks=16200
dataPrev=[]
dataNow=[]
dataAllBlocks=[]
dataAllFrames=[0]
counter=np.zeros(noOfBlocks)
flickering=0
adjBlocksListsVert=[]
adjBlocksListsHori=[]
for i in range(1,134):
    adjBlocksListsVert.append(i*120)
for i in range(1,134):
    adjBlocksListsVert.append(i*120+119)
for i in range(1,119):
    adjBlocksListsHori.append(i)
for i in range(16081,16199):
    adjBlocksListsHori.append(i)
    
period=[[[1,25],[25,50],[50,75],[75,100],[100,125],[125,150]], # BBB
        [[1,30],[30,60],[60,90],[90,120],[120,150],[150,180]], # BIC
        [[1,30],[30,60],[60,90],[90,120],[120,150],[150,180]], # BQT
        [[1,25],[25,50],[50,75],[75,100],[100,125],[125,150]], # CRN
        [[1,25],[25,50],[50,75],[75,100],[100,125],[125,150]], # DKS
        [[1,30],[30,60],[60,90],[90,120],[120,150],[150,180]], # EF1
        [[1,30],[30,60],[60,90],[90,120],[120,150],[150,180]], # EF2
        [[1,25],[25,43],[43,68],[68,81],[81,106],[106,131],[131,150]], # FOX [[0,25],[25,43],[43,75],[75,81],[81,106],[106,150-1]]
        [[1,12],[12,24],[24,36],[36,48],[48,60],[60,72],[72,84],[84,96],[96,108],[108,120],[120,132]], # KIM
        [[1,25],[25,50],[50,75],[75,100],[100,125],[125,150]], # OTC
        [[1,25],[25,50],[50,75],[75,100],[100,125],[125,150]], # SEE
        [[1,24],[24,48],[48,72],[72,87],[87,111],[111,120]]] # TEN [[0,25],[25,43],[43,75],[75,81],[81,106],[106,150-1]]
p=[25,30,30,25,25,30,30,25,12,25,25,24]
noOfSets=[6,6,6,6,6,6,6,7,11,6,6,6]

# workbook_name = 'Flickering/BigBuckBunny_H264_1_Flickering.xlsx'
# book = openpyxl.load_workbook(workbook_name)


for vid in range(4,5):
    for f in range(1,2):
        for level in range(4,5):
            filename = 'Video/' + str(Name[vid]) + str(Format[f]) + str(level) + '.yuv'
            print("Extracting Flickering Artifacts of " + filename)
            book = openpyxl.Workbook()
            sheet = book.active
            sheet['A1'] = 'Frame'
            sheet['B1'] = 'Flickering'
            sheet['A2'] = 1
            sheet['B2'] = 0
           
            # Initialise the states of each macroblock
            for i in range(0,noOfBlocks):
                    dataPrev.append('n')
                    
            for sets in range(0,noOfSets[vid]):
                
                # Reset the states of each macroblock
                if (Name[vid]=="FOX" and (sets==2 or sets==4 or sets==5)) or (Name[vid]=="TEN" and sets==4):
                    for i in range(0,noOfBlocks):
                        dataPrev.append('n')
                        
                for frame in range(period[vid][sets][0],period[vid][sets][1]):
                    YComp1, u1, v1 = YComponent(filename,H,W,frame-1)
                    YComp2, u1, v1 = YComponent(filename,H,W,frame)
                    YComp1 = YComp1.astype(np.int32)
                    YComp2 = YComp2.astype(np.int32)
                    
                    """
                        Find the number of the changes of states of each macroblock
                        within the time (video duration)
                    """
                    for j in range(0,noOfBlocks):
                        print(str(Name[vid]) + str(Format[f]) + str(level))
                        print("Getting frame " + str(frame + 1) + ", Block " + str(j))
                        b1=blockshaped(YComp1, h, w)[j].flatten()
                        b2=blockshaped(YComp2, h, w)[j].flatten()
                        blockDiff=b2-b1
                        blockDiff=pow(blockDiff,2)
                        blockDiff=sum(blockDiff)
                        # blockDiff = np.subtract(b2, b1)
                        # blockDiff = np.square(blockDiff)
                        # blockDiff = np.sum(blockDiff)
                        blockDiff /=128
                        if dataPrev[j]=='n' and blockDiff<threshold:
                            dataNow.append('n')
                        elif dataPrev[j]=='n' and blockDiff>=threshold:
                            dataNow.append('u')
                            counter[j]=1
                        if dataPrev[j]=='u' and blockDiff==0:
                            dataNow.append('n')
                            counter[j]+=1
                        elif dataPrev[j]=='u' and blockDiff>0:
                            dataNow.append('u')
                    
                    """
                        Adjust the number of the changes of states of each macroblock
                        by calculating the adjacent blocks
                    """
                    pp=0
                    if Name[vid]=="FOX" and sets==1: pp=18
                    elif Name[vid]=="FOX" and sets==3: pp=13
                    elif Name[vid]=="FOX" and sets==6: pp=19
                    elif Name[vid]=="TEN" and sets==3: pp=15
                    elif Name[vid]=="TEN" and sets==5: pp=9
                    else: pp=p[vid]
                    
                    
                    for j in range(0,noOfBlocks):
                        x=0
                        if j==0 or j==119 or j==16080 or j==16199:
                            if j==0: x=counter[0]+counter[1]+counter[120]+counter[121]
                            elif j==119: x=counter[119]+counter[118]+counter[239]+counter[238]
                            elif j==16080: x=counter[16080]+counter[16081]+counter[15960]+counter[15961]
                            elif j==16199: x=counter[16199]+counter[16198]+counter[16079]+counter[16078]
                            flickering=x/(4*pp)
                        elif j in adjBlocksListsHori:
                            if j<119:
                                x=counter[j]+counter[j-1]+counter[j+1]+counter[j+120]+counter[j+120-1]+counter[j+120+1]
                            else:
                                x=counter[j]+counter[j-1]+counter[j+1]+counter[j-120]+counter[j-120-1]+counter[j-120+1]
                            flickering=x/(6*pp)
                        elif j in adjBlocksListsVert:
                            if j%10==0:
                                x=counter[j]+counter[j-1]+counter[j-120]+counter[j+120]+counter[j-120+1]+counter[j+120+1]
                            else:
                                x=counter[j]+counter[j-1]+counter[j-120]+counter[j+120]+counter[j-120-1]+counter[j+120-1]
                            flickering=x/(6*pp)
                        else: 
                            x=counter[j]+counter[j-1]+counter[j+1]+counter[j-120]+counter[j-120-1]+counter[j-120+1]+counter[j+120]+counter[j+120-1]+counter[j+120+1]
                            flickering=x/(9*pp)
                        dataAllBlocks.append(flickering)
                        
                    dataAllFrames.append(max(dataAllBlocks))
                    sheet['A'+str(frame+2)] = frame + 1
                    sheet['B'+str(frame+2)] = dataAllFrames[frame]
                    dataPrev=dataNow
                    dataNow=[]
                    dataAllBlocks=[]
                
                counter=np.zeros(noOfBlocks)
                
            dataNow=[]
            dataPrev=[]
            dataAllBlocks=[]
            dataAllFrames=[0]
            counter=np.zeros(noOfBlocks)
            flickering=0
            book.save('Flickering/' + str(Name[vid]) + str(Format[f]) + str(level) + '_Flickering.xlsx')
            print("\n")


    