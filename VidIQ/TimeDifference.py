# -*- coding: utf-8 -*-
"""
Created on Fri Dec 20 13:44:06 2019

@author: user
"""


import cv2
import openpyxl
from openpyxl.styles import Alignment
from decimal import Decimal

Name = ['BigBuckBunny', 'BirdsInCage', 'BQTerrace', 'CrowdRun', 'DanceKiss', 'ElFuente1',
        'ElFuente2', 'FoxBird', 'Kimono1', 'OldTownCross', 'Seeking', 'Tennis']
FrameNo = [150, 180, 180, 150, 150, 180, 180, 150, 132, 150, 150, 120]
Format = ["_H264_","_SDH264HD_"]
File = ['BBB', 'BIC', 'BQT', 'CRN', 'DKS', 'EF1', 'EF2', 'FOX', 'KIM', 'OTC', 'SEE', 'TEN']


for vid in range(0,12):
    for f in range(0,2):
        for level in range(1,5):
            filename =  str(Name[vid]) + str(Format[f]) + str(level)
            cap = cv2.VideoCapture('video_bitstream/'+ filename + '.mp4')
            fps = cap.get(cv2.CAP_PROP_FPS)
            timestamps = [cap.get(cv2.CAP_PROP_POS_MSEC)]
            calc_timestamps = [0.0]
            while(cap.isOpened()):
                frame_exists, curr_frame = cap.read()
                if frame_exists:
                    timestamps.append(cap.get(cv2.CAP_PROP_POS_MSEC))
                    calc_timestamps.append(calc_timestamps[-1] + 1000/fps)
                else:
                    break
            cap.release()
            
            timestamps.pop(0)
            calc_timestamps.pop(0)
            
            workbook_name = 'Jerkiness/'+ filename + '_Jerkiness.xlsx'
            book = openpyxl.load_workbook(workbook_name)
            sheet = book.active
            sheet['A1'] = 'Frame'
            sheet['A2'] = 1
            sheet['B1'] = 'Time Difference (s)'
            sheet['B1'].alignment=Alignment(wrap_text=True)
            for i, (ts, cts) in enumerate(zip(timestamps, calc_timestamps)):
                print(filename)
                # print('Frame %d difference:'%i, '{0:.24g}'.format(abs(ts - cts)/1000))
                print('Frame %d difference:'%(i+1), Decimal(abs(ts - cts)/1000))
                sheet['A'+str(i+2)] = i+1
                sheet['B'+str(i+2)] = str(Decimal(abs(ts - cts)/1000))
            
            sheet['A'+str(FrameNo[vid]+2)]=''
            sheet['B'+str(FrameNo[vid]+2)]=''
            book.save(workbook_name)
            print('\n')
