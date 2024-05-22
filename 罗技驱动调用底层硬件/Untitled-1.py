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

# (919.2004 929.0943)
running = 1
C_x = 260218
C_y = 253500
ac = 1280
oc = 1280
cx = 1280-825
tancox = cx/oc
angle_deg = math.degrees(tancox) 
angle_deg = angle_deg * (-1)  
print(angle_deg)
thetrue_x = C_x/360*angle_deg/2 *0.988
thetrue_y = C_y/360*angle_deg*(-1) /1.25
print(thetrue_x,thetrue_y)
def on_press(key):   
    global running                                        #鼠标控制程序
    try:
        if key.char == 'p':
            Logitech.mouse.move(int(thetrue_x),int(thetrue_y))
    except AttributeError:
        pass  
thekeyborad = keyboard.Listener()
listener = keyboard.Listener(on_press=on_press)
listener.start()
while running == 1:
    a = 1