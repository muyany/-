from ctypes import windll
import numpy as np
import time
from ultralytics import YOLO
from pynput import keyboard   
import win32api,win32con
import math
import os
import time
import cv2
import DXGI

#os.add_dll_directory(r'D:\1homework\digital image processing\pythonDXGI\DXGI.pyd')

def getXY():
    for result in results:
        thenose_tensor        = result.boxes.xywh[0,0:2]                #坐标计算开始
        thenose_tensor        = thenose_tensor.cpu()
        thenose_numpy         = thenose_tensor.numpy() 
        thepoint_x,thepoint_y = thenose_numpy
        x,y                   = win32api.GetCursorPos()                  #x,y为屏幕分辨率
        themultiple_X         = x/(thetrue_size_X/2)                       #游戏缩放倍数
        C_x                   = 16360                                    #游戏鼠标移动速度为1时的周移动量
        C_y                   = 8080
        thepoint_x            = thepoint_x+960               #(2560-640)/2
        CX                    = abs(x-thepoint_x)
        if thechoice == 1:                                   #4:3
            OC                = x/themultiple_X
        if thechoice == 2:                                   #16:10    
            OC                = x/1.2/themultiple_X 
        if thechoice == 3:                                   #16:10    
            OC                = x/1.3/themultiple_X                                     
        tanCOX                = CX/OC
        tanCOX                = math.atan(tanCOX) 
        COX                   = math.degrees(tanCOX)
        if x-thepoint_x>0:
            COX = COX * (-1)
        thetrue_x             = COX*C_x/360  
        a                     = thetrue_x                 #x坐标计算结束

        AB                    = y                         
        AX                    = thepoint_y+480            #(1600-640)/2
        XB                    = abs(AB-AX)     
        themultiple_X         = x/(thetrue_size_Y/2)       #游戏缩放倍数
        OB                    = OC
        tanXOB                = XB/OB
        tanXOB                = math.atan(tanXOB)
        XOB                   = math.degrees(tanXOB) 
        if AB-AX>0:
            XOB               = XOB * (-1)
        thetrue_y             = XOB*C_y/180                  #y坐标计算结束
        b                     = thetrue_y
        return a,b
    
def on_press(key):                                           
    global running                        
    try:
        if key.char == 'p':                                  #鼠标控制程序
            for result in results:
                if len(result.boxes.xywh) != 0:
                    theTure = getXY()
                    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE,round(theTure[0]),round(theTure[1]),0,0)
                    time.sleep(0.02)
                    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0,0,0)
                    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0,0,0)
                else:
                    print("未识别到人物")

        if key.char == 'l':
            running = 0 
    except AttributeError:
            pass  

model = YOLO('175.engine',task='detect')

listener = keyboard.Listener(on_press=on_press)
listener.start()

running        = 1

thechoice      = int(input("请选择游戏分辨率比例\n1=(4:3)\n2=(16:10)\n3=(16:9)\n"))
thetrue_size_X = int(input("请输入游戏水平分辨率:")) 
thetrue_size_Y = int(input("请输入游戏垂直分辨率:"))    

size = 640
x1 = (2560-size)//2
x2 = (2560+size)//2
y1 = (1600-size)//2
y2 = (1600+size)//2
region = (x1,y1,x2,y2)
g = DXGI.capture(x1,y1,x2,y2)

while running==1:
    start   = time.time()
    img     = g.cap()
    img     = np.array(img)

    end     = time.time()
    print(1/(end-start))
    results = model.predict(img,show=False,device=0,classes=[3],verbose=True,half=True)
    
    for result in results:
        if len(result.boxes.xywh) != 0:
            thenose_tensor        = result.boxes.xywh[0,0:2]                #坐标计算开始
            thenose_tensor        = thenose_tensor.cpu()
            thenose_numpy         = thenose_tensor.numpy() 
            thepoint_x,thepoint_y = thenose_numpy
            print(thenose_numpy)
            cv2.rectangle(img, pt1=(int(thepoint_x), int(thepoint_y)), pt2=(int(thepoint_x), int(thepoint_y)),color=[0,0,255], thickness=3)    
            cv2.imshow('detect',img)
            cv2.waitKey(1)