from ultralytics import YOLO
import cv2
import numpy as np
import pyautogui
from pynput import keyboard
import ctypes
import os
import win32api
import math
import time
import torch

try:
    root = os.path.abspath(os.path.dirname(__file__))
    driver = ctypes.CDLL(f'{root}/logitech.driver.dll')
    ok = driver.device_open() == 1  # 该驱动每个进程可打开一个实例
    if not ok:
        print('Error, GHUB or LGS driver not found')
except FileNotFoundError:
    print(f'Error, DLL file not found')

class Logitech:

    class mouse:
        #code: 1:左键, 2:中键, 3:右键

        @staticmethod
        def press(code):
            if not ok:
                return
            driver.mouse_down(code)

        @staticmethod
        def release(code):
            if not ok:
                return
            driver.mouse_up(code)

        @staticmethod
        def click(code):
            if not ok:
                return
            driver.mouse_down(code)
            driver.mouse_up(code)

        @staticmethod
        def scroll(a):
            if not ok:
                return
            driver.scroll(a)

        @staticmethod
        def move(x, y):
            #相对移动, 绝对移动需配合 pywin32 的 win32gui 中的 GetCursorPos 计算位置
            if not ok:
                return
            if x == 0 and y == 0:
                return
            driver.moveR(x, y, True)

running = 1
tensor = torch.tensor([3.]).to(device=0)

def on_press(key):                                            #鼠标控制程序
    global running
    C_x = 260218 #一周移动量
    C_y = 253500
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
                    C_x = 260218                               #x坐标计算开始
                    C_y = 126965
                    cx = abs(x-thepoint_x)
                    tanCOX = cx/1223.8
                    tanCOX = math.atan(tanCOX) 
                    COX    = math.degrees(tanCOX)
                    if x-thepoint_x>0:
                        COX = COX * (-1)
                    thetrue_x = COX*C_x/360          #x坐标计算结束
                    
                    AB = y                         #y坐标计算开始
                    AX = thepoint_y
                    XB = abs(AB-AX)
                    OB = AB
                    tanXOB = XB/OB
                    tanXOB = math.atan(tanXOB)
                    if AB-AX>0:
                        tanXOB = tanXOB * (-1)
                    XOB    = math.degrees(tanXOB) #*180/math.pi
                    thetrue_y = XOB*C_y/180         #y坐标计算结束
                    if 50<cx<100:                      #准星与人物距离过近，引入坐标修正机制
                        thetrue_x = (thetrue_x/10)
                        print("距离小于100,坐标修正")
                    if cx<50:
                        thetrue_x = (thetrue_x/5)
                        print("距离小于50,坐标修正")
                    Logitech.mouse.move(round(thetrue_x),0)
                    time.sleep(0.05)
                    #Logitech.mouse.move(0,round(thetrue_y))
                    print("人物坐标",thenose_numpy)
                    print("需要移动的鼠标像素",thetrue_x,thetrue_y)
                    time.sleep(0.01)
                    Logitech.mouse.press(1)
                    Logitech.mouse.release(1)
                else:
                    print("没人或者数据未读取")
        if key.char == 'l':
            running = 0
    except AttributeError:
        pass  

#model = YOLO('yolov8n.pt')
model = YOLO(r'D:\1homework\python\Yolov8-CS2-detection\models/175.pt')


thekeyborad = keyboard.Listener()
listener = keyboard.Listener(on_press=on_press)
listener.start()
while running == 1:
    screenshot = pyautogui.screenshot()
    frame = np.array(screenshot)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = model.predict(frame,show=True,device=0,classes=[3],imgsz=2560,verbose=False)
    if running == 0:
        break

