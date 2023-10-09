"""

NAME : gui_tk

USER : admin

DATE : 9/10/2023

PROJECT_NAME : RetinaFace-FaceNet

CSDN : friklogff
"""
import cv2
import os
import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
import numpy as np

from PIL import ImageFont


def cv2AddChineseText(img, text, position, textColor=(0, 255, 0), textSize=30):
    if (isinstance(img, np.ndarray)):  # 判断是否OpenCV图片类型
        img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    # 创建一个可以在给定图像上绘图的对象
    draw = ImageDraw.Draw(img)
    # 字体的格式
    fontStyle = ImageFont.truetype(
        "simsun.ttc", textSize, encoding="utf-8")
    # 绘制文本
    draw.text(position, text, textColor, font=fontStyle)
    # 转换回OpenCV格式
    return cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)


# 加载自定义字体
font = ImageFont.truetype(r"C:\Users\ge\Desktop\test1\Cuesor\msyh.ttc", size=30)

# 加载Haar Cascade分类器
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# 创建GUI窗口
root = tk.Tk()
root.geometry('640x480')
root.title('人脸识别')

# 创建标签用于显示图像
image_label = tk.Label(root)
image_label.pack()

# 打开摄像头并捕获实时图像
cap = cv2.VideoCapture(0)

# 创建 PhotoImage 对象
photo = None

# 读取person文件夹中的图像和姓名
person_images = []
person_names = []
for filename in os.listdir('person'):
    if filename.endswith('.jpg'):
        # 使用utf-8编码打开文件
        with open(os.path.join('person', filename), 'rb') as f:
            person_images.append(cv2.imdecode(np.frombuffer(f.read(), np.uint8), cv2.IMREAD_COLOR))
        person_names.append(os.path.splitext(filename)[0])

# 循环处理摄像头捕获的图
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 转换图像格式以进行人脸检测
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 使用Haar Cascade分类器检测人脸
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    # 在图像中框出检测到的人脸
    for (x, y, w, h) in faces:
        # 检查人脸是否属于person文件夹中的某个人
        found_person = False
        for i in range(len(person_images)):
            person_image = person_images[i]
            person_name = person_names[i]
            # 将person图像转换为灰度图像以进行比较
            person_gray = cv2.cvtColor(person_image, cv2.COLOR_BGR2GRAY)
            # 检查是否存在与person图像相匹配的人脸
            match = cv2.matchTemplate(gray[y:y + h, x:x + w], person_gray, cv2.TM_CCOEFF_NORMED)
            if match.max() > 0.8:
                print(person_name)
                found_person = True
                # 在图像中框出人脸并显示姓名
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)
                # 在图像中框出人脸并显示姓名
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)
                frame = cv2AddChineseText(frame, person_name, (x + (w / 2) - 10, y - 30), (0, 255, 255), 30)
                break

        # 如果没有找到匹配的人脸，则在图像中框出人脸但不显示姓名
        if not found_person:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # 将图像转换为PIL Image格式以在GUI中显示

    image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    photo = ImageTk.PhotoImage(image)

    # 更新标签以显示图像
    image_label.configure(image=photo)
    image_label.image = photo

    # 处理GUI事件以避免程序挂起
    root.update()
# 关闭摄像头并销毁窗口
cap.release()
cv2.destroyAllWindows()