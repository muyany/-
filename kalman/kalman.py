import numpy as np
from kalmanfilter import KalmanFilter
import cv2
from ultralytics import YOLO
import DXGI
from pynput import keyboard   
import time
import win32api,win32con
import math

def getXY():
    for result in results:
        thechoice = 2
        thetrue_size_X = 2560
        thetrue_size_Y = 1600
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

kf = KalmanFilter()

listener = keyboard.Listener(on_press=on_press)
listener.start()

running        = 1

#thechoice      = int(input("请选择游戏分辨率比例\n1=(4:3)\n2=(16:10)\n3=(16:9)\n"))
#thetrue_size_X = int(input("请输入游戏水平分辨率:")) 
#thetrue_size_Y = int(input("请输入游戏垂直分辨率:"))    

thechoice = 2
thetrue_size_x = 2560
thetrue_size_y = 1600

size = 640
x1 = (2560-size)//2
x2 = (2560+size)//2
y1 = (1600-size)//2
y2 = (1600+size)//2
region = (x1,y1,x2,y2)
g = DXGI.capture(x1,y1,x2,y2)

while running == 1:
    img     = g.cap()
    img_np     = np.array(img)
    results = model.predict(img_np,show=False,device=0,classes=[3],verbose=True,half=True)
    for result in results:
        if len(result.boxes.xyxy) != 0:
            for box in result.boxes.xyxy:
                theTure = getXY()
                win32api.mouse_event(win32con.MOUSEEVENTF_MOVE,round(theTure[0]),round(theTure[1]),0,0)
                time.sleep(0.02)
                thehead_tensor        = box[0:4]                #坐标计算开始
                thehead_tensor        = thehead_tensor.cpu()
                thehead_numpy         = thehead_tensor.numpy()
                x1,y1,x2,y2           = thehead_numpy 
                cv2.rectangle(img, 
                              pt1 = (int(x1), int(y1)),
                              pt2 = (int(x2), int(y2)),
                              color=[0,0,255],
                              thickness=3)
                predicted = kf.predict(((x1+x2)//2),((y1+y2)//2))
                cv2.circle(img, (predicted[0], predicted[1]), 20, (255, 0, 0), 4)
    cv2.imshow('img',img)
    cv2.waitKey(1)