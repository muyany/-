import os
import time

os.getcwd()
os.add_dll_directory(r'D:\1homework\digital image processing\pythonDXGI\DXGI.pyd')
from ctypes import windll
import cv2
import numpy as np
windll.winmm.timeBeginPeriod(1)
stop = windll.kernel32.Sleep
import cv2
import DXGI
import torch
g = DXGI.capture(0,0,2560,1600)  # 屏幕左上角 到 右下角  （x1, y1 ,x2 ,y2)

while True:
    current_time = time.time()
    img = g.cap()
    img = np.array(img)
    #img = cv2.cvtColor(img,cv2.COLOR_BGRA2BGR)
    last_time=time.time()
    time_used = last_time - current_time
    print(time_used)
    current_time, last_time=0, 0
    cv2.imshow('c',img)
    cv2.waitKey(1)

