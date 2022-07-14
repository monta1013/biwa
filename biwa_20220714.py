#!/usr/bin/env python
# coding: utf-8

import cv2
import datetime
import os
import matplotlib as plt
import numpy as np
import tkinter
import time
from PIL import Image
import sys
from PyQt5.QtWidgets import QApplication,QWidget,QPushButton
import numpy as np

t_delta = datetime.timedelta(hours=9)
JST = datetime.timezone(t_delta, 'JST')
now = datetime.datetime.now(JST)
print(repr(now))
d = now.strftime('%Y/%m/%d %H:%M:%S')
print(d)  


date = now.strftime('%Y%m%d_%H%M%S') 
date1 = now.strftime('%Y%m%d') 
path1 = "date/" + date
path2 = "date/" + date1
basename = os.path.basename(path1)
dirname = os.path.dirname(path1)
print(path1)
print(basename)
print(dirname)
print(dirname +"/"+ basename)

def gstreamer_pipeline(sensor_id=0, exposure=500000, capture_width=1280, capture_height=720, 
                       display_width=640, display_height=360, framerate=60, flip_method=0):    
    pipeline = f"nvarguscamerasrc sensor-id={sensor_id} exposuretimerange='{int(exposure)} {int(exposure)+1}' !                video/x-raw(memory:NVMM), width=(int){capture_width}, height=(int){capture_height},                 framerate=(fraction){framerate}/1 ! nvvidconv flip-method={flip_method} !                 video/x-raw, width=(int){display_width}, height=(int){display_height}, format=(string)BGRx !                 videoconvert ! video/x-raw, format=(string)BGR ! appsink"
    return(pipeline)

def main():
    pipeline = gstreamer_pipeline(exposure=1E+6)
    print(pipeline)

    cap = cv2.VideoCapture(pipeline, cv2.CAP_GSTREAMER)
    old_time = time.time()

    if cap.isOpened():
        try:
            while True:
                now = datetime.datetime.now(JST)
                #print(repr(now))

                d = now.strftime('%Y/%m/%d %H:%M:%S')
                ret,frame = cap.read()
                ret,frame2= cap.read()

                #print(ret)
                #reframe = cv2.resize(frame, dsize=(1280,720))

                #cv2.putText(frame, text = d,
                #           org = (0, 50),
                #          fontFace = cv2.FONT_HERSHEY_PLAIN,
                #         fontScale = 3, 
                    #        color = (0, 255, 0),
                    #       thickness = 2, 
                    #      lineType = cv2.LINE_AA)
                
                cv2.rectangle(frame2, (500, 10), (620, 60), (0, 255, 0))
                cv2.putText(frame2,
                            'cap0',
                            (520, 40),
                            cv2.FONT_HERSHEY_SIMPLEX, 
                            1.0, 
                            (255, 255, 255),
                            thickness=2)

                cv2.rectangle(frame2, (500, 70), (620, 120), (0, 255, 0))
                cv2.putText(frame2,'cap1',(520, 100),cv2.FONT_HERSHEY_SIMPLEX,1.0,(255, 255, 255), thickness=2)
            
                cv2.rectangle(frame2, (500, 130), (620, 180), (0, 255, 0))
                cv2.putText(frame2,'cap2',(520, 160),cv2.FONT_HERSHEY_SIMPLEX,1.0,(255, 255, 255), thickness=2)

                cv2.rectangle(frame2, (500, 190), (620, 240), (0, 255, 0))
                cv2.putText(frame2,'cap3',(520, 220),cv2.FONT_HERSHEY_SIMPLEX,1.0,(255, 255, 255), thickness=2)

                cv2.rectangle(frame2, (500, 250), (620, 300), (0, 255, 0))
                cv2.putText(frame2,'quit',(520, 280),cv2.FONT_HERSHEY_SIMPLEX,1.0,(255, 255, 255), thickness=2)

                cv2.imshow('window1', frame2)
                def onMouse(event, x, y, flags, params):
    
                    if event == cv2.EVENT_LBUTTONDOWN:
                        print(x, y)
                        
                        now = datetime.datetime.now(JST)
                        date2 = now.strftime('%Y%m%d%H%M%S')
                        
                        if(500<x<620 and 10<y<60):
                            path = dirname  + "/" + date2 + "_label_0_" + ".jpg"
                            cv2.imwrite(path,frame)
                        elif (500<x<620 and 70<y<120):
                            path = dirname  + "/" + date2 + "_label_1_" + ".jpg"
                            cv2.imwrite(path,frame)
                        elif (500<x<620 and 130<y<180):
                            path = dirname  + "/" + date2 + "_label_2_" + ".jpg"
                            cv2.imwrite(path,frame)
                        elif (500<x<620 and 190<y<240):
                            path = dirname  + "/" + date2 + "_label_3_" + ".jpg"
                            cv2.imwrite(path,frame)
                        elif (500<x<620 and 250<y<300):
                            print("break")
                            exit()
                cv2.setMouseCallback('window1', onMouse)
            
                k = cv2.waitKey(1) & 0xFF

                if k  == ord('p'):
                    now = datetime.datetime.now(JST)
                    date2 = now.strftime('%Y%m%d%H%M%S')
                    path = dirname  + "/" + date2 + ".jpg"
                    cv2.imwrite(path,frame)
                # img = cv2.imread(path)
                    #cv2.imshow('sample', img)
                # cv2.setMouseCallback('sample', onMouse)
                #  cv2.waitKey(0)
                    
                elif k == ord('q'):
                    break
            
        finally:
            cap.release()
            cv2.destroyAllWindows()
    else:
        print("Error: Unable to open camera")


if __name__ == "__main__":
    main()

"""
# In[5]:


camera = cv2.VideoCapture(1)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280) # カメラ画像の横幅を1280に設定
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720) # カメラ画像の縦幅を720に設定
while True:
    now = datetime.datetime.now(JST)
    print(repr(now))
    d = now.strftime('%Y/%m/%d %H:%M:%S')
    ret,frame = camera.read()
    reframe = cv2.resize(frame, dsize=(1280,720))
    cv2.putText(reframe, text = d,
                org = (0, 50),
                fontFace = cv2.FONT_HERSHEY_PLAIN,
                fontScale = 4, 
                color = (0, 255, 0),
                thickness = 2, 
                lineType = cv2.LINE_AA)
    
    cv2.imshow('window1', reframe)
    k = cv2.waitKey(1) & 0xFF
    if k  == ord('p'):
        now = datetime.datetime.now(JST)
        date2 = now.strftime('%Y%m%d%H%M%S') 
        path = dirname  + "/" + date2 + ".jpg"        
        cv2.imwrite(path,reframe)
    elif k == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()


# In[ ]:





# In[ ]:


camera = cv2.VideoCapture(0, cv2.CAP_MSMF)
camera.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
camera.set(cv2.CAP_PROP_FPS, 60)           # カメラFPSを60FPSに設定
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280) # カメラ画像の横幅を1280に設定
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720) # カメラ画像の縦幅を720に設定


# In[ ]:





# In[ ]:





# In[ ]:



"""

