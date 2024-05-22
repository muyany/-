import win32api
from pynput import keyboard
import ctypes
import os
import time
import winsound

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

        """
        code: 1:左键, 2:中键, 3:右键
        """

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
            """
            a:没搞明白
            """
            if not ok:
                return
            driver.scroll(a)

        @staticmethod
        def move(x, y):
            """
            相对移动, 绝对移动需配合 pywin32 的 win32gui 中的 GetCursorPos 计算位置
            pip install pywin32 -i https://pypi.tuna.tsinghua.edu.cn/simple
            x: 水平移动的方向和距离, 正数向右, 负数向左
            y: 垂直移动的方向和距离
            """
            if not ok:
                return
            if x == 0 and y == 0:
                return
            driver.moveR(x, y, True)

    class keyboard:

        """
        键盘按键函数中，传入的参数采用的是键盘按键对应的键码
        code: 'a'-'z':A键-Z键, '0'-'9':0-9, 其他的没猜出来
        """

        @staticmethod
        def press(code):

            if not ok:
                return
            driver.key_down(code)

        @staticmethod
        def release(code):
            if not ok:
                return
            driver.key_up(code)

        @staticmethod
        def click(code):
            if not ok:
                return
            driver.key_down(code)
            driver.key_up(code)


running = 1
def on_press(key):
    global running
    try:
        if key.char == 'p':
            Logitech.mouse.move(10000,0) 
                       #=1  x = 260218           X=16.3069      Y=109.575988
        if key.char == 'o':
            Logitech.mouse.move(round(10000*0.5),0)  
            Logitech.mouse.move(round(10000*0.3),0)
            Logitech.mouse.move(round(10000*0.2),0)                         #人物坐标 [     801.66      883.96] 屏幕坐标[1280,800]
        if key.char == 'i':
            Logitech.mouse.move(0,10000)
            time.sleep(0.001)
            Logitech.mouse.move(10000,0)    
        if key.char == 'l':
            Logitech.mouse.move(10000,0)   
        if key.char == 'k':
            Logitech.mouse.move(20000,0) 
        if key.char == 'j':
            Logitech.mouse.move(0,20000)   
    except AttributeError:
        pass  
thekeyborad = keyboard.Listener()
listener = keyboard.Listener(on_press=on_press)
listener.start()

while running == 1:
    x,y = win32api.GetCursorPos()

