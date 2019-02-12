#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
opencv 连接caram 取流
'''

import cv2
# url = 'rtsp://admin:password@192.168.1.104:554/11'
url = "rtsp://admin:oeasy123@192.168.1.106:554/LiveMedia/ch1/Media1"
cap = cv2.VideoCapture(url)
while cap.isOpened():
    # Capture frame-by-frame  
    ret, frame=cap.read()
    # Display the resulting frame  
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# When everything done, release the capture  
cap.release()
cv2.destroyAllWindows()
