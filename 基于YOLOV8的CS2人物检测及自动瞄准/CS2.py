from ultralytics import YOLO
import cv2
import numpy as np
import pyautogui
from pynput import keyboard                                                                                      记得把鼠标dpi改成1000
import win32api,win32con
import math

running = 1                                           #控制参数

def on_press(key):                                            #鼠标控制程序
    global running
    C_x = 16364 #一周移动量         #16:10 dpi = 1000*1 C_x（2048*1536） = 16364       16.9 C_x = 18000   不同分辨率不同比例需要重新计算一周移动量 
    try:
        if key.char == 'p':
            for result in results:
                #b = box.xywh  # get box coordinates in (top, left, bottom, right) format
                c = result.boxes.xywh      # get the class name
                if len(result.boxes.xywh) != 0:
                    thenose_tensor        = result.boxes.xywh[0,0:2]
                    thenose_tensor        = thenose_tensor.cpu()
                    thenose_numpy         = thenose_tensor.numpy() 
                    thepoint_x,thepoint_y = thenose_numpy
                    x,y                   = win32api.GetCursorPos()
                    C_x                   = 16364                          #x坐标计算开始
                    C_y                   = 8080
                    cx                    = abs(x-thepoint_x)
                    tanCOX                = cx/x
                    tanCOX                = math.atan(tanCOX) 
                    COX                   = math.degrees(tanCOX)
                    if x-thepoint_x>0:
                        COX = COX * (-1)
                    thetrue_x             = COX*C_x/360  
                    
                    AB  = y                         #y坐标计算开始
                    AX = thepoint_y
                    XB = abs(AB-AX)
                    OB = x
                    tanXOB = XB/OB
                    tanXOB = math.atan(tanXOB)
                    XOB    = math.degrees(tanXOB) 
                    if AB-AX>0:
                        XOB = XOB * (-1)
                    thetrue_y = XOB*C_y/180        #y坐标计算结束
                    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE,round(thetrue_x),0,0,0)
                    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE,0,round(thetrue_y),0,0)
                else:
                    print("没人或者数据未读取")
        if key.char == 'j':                #一周移动量检测
            win32api.mouse_event(win32con.MOUSEEVENTF_MOVE,0,8080,0,0)
        if key.char == 'k': 
            win32api.mouse_event(win32con.MOUSEEVENTF_MOVE,0,100,0,0)
        if key.char == 'o': 
            win32api.mouse_event(win32con.MOUSEEVENTF_MOVE,0,10,0,0)
        if key.char == 'l':                           #按l退出
            running = 0
    except AttributeError:
            pass  

model = YOLO(r'D:\1homework\python\Yolov8-CS2-detection\models/175.pt')

thekeyborad = keyboard.Listener()
listener = keyboard.Listener(on_press=on_press)
listener.start()
while running == 1:
    screenshot = pyautogui.screenshot()
    frame = np.array(screenshot)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = model.predict(frame,show=True,device=0,classes=[3],imgsz=2560,verbose=False)           #classes 0: CT  1: T  2: CTh  3: Th
    if running == 0:
        break

