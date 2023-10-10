"""

NAME : add_face

USER : admin

DATE : 10/10/2023

PROJECT_NAME : RetinaFace-FaceNet

CSDN : friklogff
"""
import os
import cv2
from PIL import Image, ImageTk
import numpy as np
import pymysql

import try_7
from retinaface import Retinaface


class Database:
    def __init__(self):
        self.conn = pymysql.connect(host="127.0.0.1",
                                    port=3306,
                                    user="root",
                                    password="1300982918",
                                    database="rlsb")
        self.cursor = self.conn.cursor()

    def insert_name(self, name):
        query = "INSERT INTO name_table (name) VALUES (%s)"
        self.cursor.execute(query, (name,))
        self.conn.commit()

    def query_name(self):
        query = "SELECT name FROM name_table"
        self.cursor.execute(query)
        return [row[0] for row in self.cursor.fetchall()]

    def query_record(self):
        query = "SELECT * FROM record_table"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def insert_record(self, username):
        import datetime
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        insert_query = "INSERT INTO record_table (name, check_time) VALUES (%s, %s)"
        self.cursor.execute(insert_query, (username, current_time))
        self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()

def makeDir():
    if not os.path.exists("face_dataset"):
        os.mkdir("face_dataset")
    if not os.path.exists("FaceData"):
        os.mkdir("FaceData")

def getFace(name):
    cap = cv2.VideoCapture('R.mp4')
    num = 0
    while cap.isOpened():
        ret_flag, Vshow = cap.read()  # 得到每帧图像
        cv2.imshow("Capture_Test", Vshow)  # 显示图像
        k = cv2.waitKey(1) & 0xFF  # 按键判断
        if k == ord('s'):  # 保存
            cv2.imwrite("face_dataset/" + name + "_" + str(num) + ".jpg", Vshow)
            print("success to save" + str(num) + ".jpg")
            print("-------------------")
            num += 1
        elif k == ord(' '):  # 退出
            break
    #释放摄像头
    cap.release()
    #释放内存
    cv2.destroyAllWindows()


def encode_faces():
    '''
    在更换facenet网络后一定要重新进行人脸编码，运行encoding.py。
    '''
    retinaface = Retinaface(1)

    list_dir = os.listdir("face_dataset")
    image_paths = []
    names = []
    user_db = Database()
    for name in list_dir:
        image_paths.append("face_dataset/" + name)
        names.append(name.split("_")[0])
        print(name.split("_")[0],names)
        try:
            user_db.insert_name(name.split("_")[0])
        except Exception as e:
            print(e)

    retinaface.encode_face_dataset(image_paths, names)
    user_db.close()
    return "Encoding complete!"

def add_face(name, names):
    makeDir()
    getFace(name)
    encode_faces()
