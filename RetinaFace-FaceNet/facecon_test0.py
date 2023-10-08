import dlib
import cv2
import numpy as np
# 加载人脸关键点检测模型
predictor_model = "shape_predictor_68_face_landmarks.dat"
predictor = dlib.shape_predictor(predictor_model)

# 加载人脸检测器
face_detector = dlib.get_frontal_face_detector()

# 打开摄像头
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 将图像转换为灰度图
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 使用人脸检测器检测人脸
    faces = face_detector(gray)

    for face in faces:
        # 使用关键点检测器检测关键点
        landmarks = predictor(frame, face)

        # 获取关键点坐标
        points = [(p.x, p.y) for p in landmarks.parts()]

        # 提取眉毛、眼睛和嘴巴的坐标
        left_eyebrow = points[17:22]
        right_eyebrow = points[22:27]
        left_eye = points[36:42]
        right_eye = points[42:48]
        mouth = points[48:68]

        # 计算眉毛、眼睛和嘴巴的轮廓
        eyebrow_contour = cv2.convexHull(np.array(left_eyebrow + right_eyebrow))
        eye_contour = cv2.convexHull(np.array(left_eye + right_eye))
        mouth_contour = cv2.convexHull(np.array(mouth))

        # 绘制轮廓
        cv2.drawContours(frame, [eyebrow_contour], -1, (0, 255, 0), 2)
        cv2.drawContours(frame, [eye_contour], -1, (0, 255, 0), 2)
        cv2.drawContours(frame, [mouth_contour], -1, (0, 255, 0), 2)

    # 显示带有面部表情分析的图像
    cv2.imshow('Facial Expression Analysis', frame)

    # 按下 'q' 键退出循环
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 释放资源
cap.release()
cv2.destroyAllWindows()
