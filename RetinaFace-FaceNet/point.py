from imutils import face_utils
import dlib
import imutils
import cv2
import os
import math
import time
import numpy as np
def write_img(img):
    cv2.imwrite('./capsave/'+str(time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime()))+'.jpg',img)
def det_68():
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("./shape_predictor_68_face_landmarks.dat")


    pics="images/"
    all_list=os.listdir(pics)

    for e in all_list:
        # image = cv2.imread(pics+e)
        image = cv2.imread("./4.jpg")


        # image = imutils.resize(image, width=112)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        rects = detector(gray, 1)


        # enumerate()方法用于将一个可遍历的数据对象(列表、元组、字典)组合
        # 为一个索引序列，同时列出 数据下标 和 数据 ，一般用在for循环中
        for(i, rect) in enumerate(rects):
            shape = predictor(gray, rect)  # 标记人脸中的68个landmark点
            shape = face_utils.shape_to_np(shape)  # shape转换成68个坐标点矩阵
            (mStart, mEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS["mouth"]

            (x, y, w, h) = face_utils.rect_to_bb(rect)  # 返回人脸框的左上角坐标和矩形框的尺寸
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

            cv2.putText(image, "Face #{}".format(i + 1), (x - 10, y - 10),
                         cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            # landmarksNum = 0;
