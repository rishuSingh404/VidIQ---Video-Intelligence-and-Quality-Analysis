# -*- coding: utf-8 -*-
"""
Created on Sat Dec 21 03:21:11 2019

@author: user
"""

import openpyxl
from decimal import Decimal
from Functions import jerkiness

# Run MotionIntensity.py first before running this file

Name = ['BigBuckBunny', 'BirdsInCage', 'BQTerrace', 'CrowdRun', 'DanceKiss', 'ElFuente1',
        'ElFuente2', 'FoxBird', 'Kimono1', 'OldTownCross', 'Seeking', 'Tennis']
FrameNo = [150, 180, 180, 150, 150, 180, 180, 150, 132, 150, 150, 120]
Format = ["_H264_","_SDH264HD_"]
VideoDuration=[6, 6, 6, 6, 6, 6, 6, 6, 5.5, 6, 6, 5]
File = ['BBB', 'BIC', 'BQT', 'CRN', 'DKS', 'EF1', 'EF2', 'FOX', 'KIM', 'OTC', 'SEE', 'TEN']
columns=['B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M']


# sheet.column_dimensions['A'].width = 15

dataMI=[]
dataTD=[]
            
for vid in range(0,12):
    for f in range(0,2):
        for level in range(1,5):
            filename =  str(Name[vid]) + str(Format[f]) + str(level)
            workbook_name = 'Jerkiness/'+ filename + '_Jerkiness.xlsx'
            book = openpyxl.load_workbook(workbook_name)
            sheet = book.active
            
            sheet['D1'] = 'Jerkiness'
            sheet.column_dimensions['C'].width = 20
            # Read Motion Intensity and Time Difference from the file
            # Values read from the file must be stored in the lists first
            for row in range(2,FrameNo[vid]+2):
                dataMI.append(float(Decimal(sheet['C'+str(row)].value)))
                dataTD.append(float(Decimal(sheet['B'+str(row)].value)))
            
            # Write the data into the file
            for row in range(2,FrameNo[vid]+2):
                sheet['D'+str(row)]=jerkiness(0.01, dataMI[row-2], dataTD[row-2])
                print(filename + ': ')
                print(sheet['D'+str(row)].value)
            
            book.save(workbook_name)
            print('\n')
            
            dataMI=[]
            dataTD=[]
