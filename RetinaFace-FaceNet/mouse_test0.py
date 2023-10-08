import dlib
import cv2
import numpy as np

# 初始化
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# 颜色列表
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 255, 255)]

# 定义嘴巴关键点的索引
mouth_indices = list(range(48, 68))  # 48到67是嘴巴区域的关键点索引

# 定义嘴巴宽度阈值，根据需要进行调整
mouth_open_threshold = 15.0  # 调整此阈值以适应您的情况

# 打开摄像头
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 检测人脸
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)

    for face in faces:
        landmarks = predictor(gray, face)

        # 绘制人脸边界框
        x, y, w, h = face.left(), face.top(), face.width(), face.height()
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # 绘制关键点
        for i, point in enumerate(landmarks.parts()):
            x, y = point.x, point.y
            color = colors[i % len(colors)]
            cv2.circle(frame, (x, y), 2, color, -1)

        # 提取嘴巴关键点的坐标
        mouth_points = np.array([(landmarks.part(i).x, landmarks.part(i).y) for i in mouth_indices])

        # 计算嘴巴的宽度
        mouth_width = np.linalg.norm(mouth_points[6] - mouth_points[0])

        # 如果嘴巴宽度超过阈值，认为正在张嘴
        if mouth_width > mouth_open_threshold:
            cv2.putText(frame, "Mouth Open", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow("Frame", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
