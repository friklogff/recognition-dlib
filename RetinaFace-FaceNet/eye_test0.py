
import dlib
import cv2
import numpy as np


# 计算眼睛长宽比
def eye_aspect_ratio(eye):
    A = np.linalg.norm(eye[1] - eye[5])
    B = np.linalg.norm(eye[2] - eye[4])
    C = np.linalg.norm(eye[0] - eye[3])
    ear = (A + B) / (2.0 * C)
    return ear


# 获取最大的人脸
def largest_face(dets):
    if len(dets) == 1:
        return 0

    face_areas = [(det.right() - det.left()) *
                  (det.bottom() - det.top()) for det in dets]
    largest_area = face_areas[0]
    largest_index = 0
    for index in range(1, len(dets)):
        if face_areas[index] > largest_area:
            largest_index = index
            largest_area = face_areas[index]
    return largest_index


# 初始化探测器和预测器
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# 获取视频流
cap = cv2.VideoCapture(0)

# 初始化帧计数器和眨眼计数器
frame_counter = 0
blink_counter = 0

while True:
    # 获取当前帧
    ret, frame = cap.read()
    if not ret:
        break

    # 转换为灰度图
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 检测人脸
    faces = detector(gray, 0)

    # 检测到人脸
    if len(faces) > 0:
        # 获取最大的人脸
        index = largest_face(faces)
        face = faces[index]

        # 获取特征点
        landmarks = np.matrix([[p.x, p.y] for p in predictor(frame, face).parts()])

        # 提取左右眼点
        left_eye = landmarks[42:48]
        right_eye = landmarks[36:42]

        # 计算EAR
        left_ear = eye_aspect_ratio(left_eye)
        right_ear = eye_aspect_ratio(right_eye)
        ear = (left_ear + right_ear) / 2.0

        # 判断是否眨眼
        if ear < 0.21:
            frame_counter += 1
            status = "Blinking"

        else:
            # 眨眼次数判断
            if frame_counter >= 3:
                blink_counter += 1
            frame_counter = 0
            status = "Open"

        # 显示眨眼结果
        cv2.putText(frame, "Blinks: {}".format(blink_counter), (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.putText(frame, "EAR: {:.2f}".format(ear), (300, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.putText(frame, "Status: {}".format(status), (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

    # 显示画面
    cv2.imshow("Frame", frame)

    # 按Q退出
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

# 释放资源并关闭窗口
cap.release()
cv2.destroyAllWindows()
