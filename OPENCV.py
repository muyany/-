import cv2
import pyautogui
import time
screen_width, screen_height = pyautogui.size()
path = r'C:\Users\jinyu\Desktop\20240205-DSC02145.JPG'        # window 读取文件可以用\，但是在字符串中\是被当作转义字符来使用，经过转义之后可能就找不到路径的资源了,路径前面加r
img = cv2.imread(path)
cv2.namedWindow('Demo',cv2.WINDOW_NORMAL)     #创建一个具有合适名称和大小的窗口，以在屏幕上显示图像和视频
face_detect = cv2.CascadeClassifier(r'D:\Python\Lib\site-packages\cv2\data\haarcascade_frontalface_default.xml')

# 灰度处理           图像灰度化的目的是为了简化矩阵，提高运算速度
gray = cv2.cvtColor(img, code=cv2.COLOR_BGR2GRAY)

face_zone = face_detect.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
print('识别人脸的信息：',face_zone)

# 获取图像在代码中的尺寸
size = img.shape  # 图像宽度（像素数）

# 绘制矩形和圆形检测人脸
for x, y, w, h in face_zone:
    center_x = (x+w/2) // (size[1]/screen_width)
    center_y = (y+h/2) // (size[0]/screen_height)
    # 绘制矩形人脸区域 thickness表示线的粗细
    cv2.rectangle(img, pt1=(x, y), pt2=(x+w, y+h),color=[0,0,255], thickness=3)
    #pyautogui.moveTo(center_x,center_y)
    pyautogui.moveTo(center_x,center_y)
    print(center_x,center_y)
    
#改变图像尺寸
# width = 2560
# height = 1600
# dim = (width, height)
# gray = cv2.resize(gray,dim)
cv2.imshow("Demo",img)

#等待显示
cv2.waitKey(0)
cv2.destroyAllWindows()


#保存文件
#cv2.imwriter("asd.jpg",gray)
