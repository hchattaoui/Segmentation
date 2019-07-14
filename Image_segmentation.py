
# coding: utf-8


#!/usr/bin/env python



import cv2
import sys
import numpy as np



try:
    video_file_path = str(sys.argv[1])
    fps = int(sys.argv[2])
    width = int(sys.argv[3])
    height = int(sys.argv[4])
    monochrome = (str(sys.argv[5]) == 'True')
except:
    video_file_path = 'video_1.mp4'
    fps = 20
    width = 1500
    height = 900
    monochrome = False


def filter_frame(img_rgb):
    
    img = cv2.cvtColor(img_rgb,cv2.COLOR_RGB2HSV)
    r,g,b=cv2.split(img)
    
    equalize1= cv2.equalizeHist(r)
    equalize2= cv2.equalizeHist(g)
    equalize3= cv2.equalizeHist(b)
    equalize=cv2.merge((r,g,b))
    equalize = cv2.cvtColor(equalize,cv2.COLOR_RGB2GRAY)

    ret,thresh_image = cv2.threshold(equalize,0,255,cv2.THRESH_OTSU+cv2.THRESH_BINARY)
    equalize= cv2.equalizeHist(thresh_image)
    
    mask = np.zeros(img_rgb.shape,np.uint8)
    new_image = cv2.bitwise_and(img_rgb, img_rgb, mask = equalize)
    
    return new_image


cap = cv2.VideoCapture(video_file_path)
ret, frame = cap.read()
if (cap.isOpened()== False): 
    print("Error opening video stream or file")

while(cap.isOpened()):
    prev_frame=frame[:]
    ret, frame = cap.read()

    cv2.namedWindow('frame',cv2.WINDOW_NORMAL)
    cv2.resizeWindow('frame', (width,height))

    if monochrome == True:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    if ret == True:
        frame = filter_frame(frame)
        cv2.imshow('frame',frame)
        key = cv2.waitKey(fps)

        if key == ord('p'):
            key = cv2.waitKey(0)

            if key == ord('b'):
                cv2.imshow('frame',prev_frame)
                key = cv2.waitKey(0)
    else:
        break
        
    if key==ord('q'):
        break;


cap.release()

cv2.destroyAllWindows()


