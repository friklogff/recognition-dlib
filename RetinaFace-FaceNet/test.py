# -*- coding = utf-8 -*-
"""
# @Time : 2023/6/30 15:20
# @Author : FriK_log_ff 374591069
# @File : enperdict.py
# @Software: PyCharm
# @Function: 请输入项目功能
"""
import time

import cv2
import numpy as np

from retinaface import Retinaface
import dlib


def _largest_face(dets):
    if len(dets) == 1:
        return 0
    face_areas = [(det.right() - det.left()) * (det.bottom() - det.top()) for det in dets]
    largest_area = face_areas[0]
    largest_index = 0
    for index in range(1, len(dets)):
        if face_areas[index] > largest_area:
            largest_index = index
            largest_area = face_areas[index]
    print("largest_face index is {} in {} faces".format(largest_index, len(dets)))
    return largest_index


# 计算眼睛的长宽比：eye aspect ratio (EAR)
def _eye_aspect_ratio(eye):
    A = np.linalg.norm(eye[1] - eye[5])
    B = np.linalg.norm(eye[2] - eye[4])
    C = np.linalg.norm(eye[0] - eye[3])
    ear = (A + B) / (2.0 * C)
    return ear





class LiveVideoDetector:
    def __init__(self, video_path, video_save_path="", video_fps=25.0, use_camera=False):
        if use_camera:
            self.capture = cv2.VideoCapture(0)
        else:
            self.capture = cv2.VideoCapture(video_path)
        self.video_save_path = video_save_path
        if video_save_path != "":
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            size = (int(self.capture.get(cv2.CAP_PROP_FRAME_WIDTH)), int(self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
            self.out = cv2.VideoWriter(video_save_path, fourcc, video_fps, size)
        ref, frame = self.capture.read()
        if not ref:
            raise ValueError("未能正确读取摄像头（视频），请注意是否正确安装摄像头（是否正确填写视频路径）。")
        self.fps = 0.0
        self.frame_counter = 0
        self.blink_counter = 0
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
        self.flag = 0
        self.fname = None
        self.retinaface = Retinaface()

    def process_frame(self):
        t1 = time.time()
        ref, frame = self.capture.read()
        if not ref:
            return None
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.detector(gray, 0)
        # 集成眨眼检测
        if len(faces) != 0:
            largest_index = _largest_face(faces)
            face_rectangle = faces[largest_index]
            landmarks = np.matrix([[p.x, p.y] for p in self.predictor(frame, face_rectangle).parts()])
            left_eye = landmarks[42:48]
            right_eye = landmarks[36:42]
            EAR_left = _eye_aspect_ratio(left_eye)
            EAR_right = _eye_aspect_ratio(right_eye)
            ear = (EAR_left + EAR_right) / 2.0
            if ear < 0.21:
                self.frame_counter += 1
                status = "Blinking"
            else:
                if self.frame_counter >= 3:
                    self.blink_counter += 1
                self.frame_counter = 0
                status = "Open"
            cv2.putText(frame, "Blinks: {}".format(self.blink_counter), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                        (0, 0, 255), 2)
            cv2.putText(frame, "EAR: {:.2f}".format(ear), (300, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            cv2.putText(frame, "Status: {}".format(status), (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
            if self.blink_counter >= 2:  # If blinks are more than the threshold, perform face recognition
                self.flag = 1
                cv2.putText(frame, "Liveness: Yes", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            else:
                self.flag = 0
                cv2.putText(frame, "Liveness: No", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # 进行检测
        # re = self.retinaface.live_detect_image(frame, self.flag)
        old_image = self.retinaface.live_detect_image(frame, self.flag)
        # old_image=re[0]
        # fname =re[1]
        frame = np.array(old_image)
        # RGBtoBGR满足opencv显示格式
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        # 计算fps
        self.fps = (self.fps + (1. / (time.time() - t1))) / 2
        print("fps= %.2f" % (self.fps))
        frame = cv2.putText(frame, "fps= %.2f" % (self.fps), (300, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        if self.video_save_path != "":
            self.out.write(frame)
        return frame

    def release(self):
        print("Video Detection Done!")
        self.capture.release()
        if self.video_save_path != "":
            print("Save processed video to the path:" + self.video_save_path)
            self.out.release()

    def get_blink_counter(self):
        return self.blink_counter

    def get_fname(self):
        return self.fname


# 开启摄像头实时进行人脸识别
# video_path = 'input/blink.mp4'
video_path = 0
detector = LiveVideoDetector(video_path)
while True:
    flag = detector.get_blink_counter()
    # fname = detector.get_fname()
    # print(flag, fname)
    frame = detector.process_frame()
    if frame is None:
        break
    cv2.imshow("frame", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    if flag == 2:
        cv2.imwrite("last_frame.png", frame)
        # print(fname)
        break
detector.release()
cv2.destroyAllWindows()
