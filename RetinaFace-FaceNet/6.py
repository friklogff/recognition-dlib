"""

NAME : 6

USER : admin

DATE : 12/10/2023

PROJECT_NAME : RetinaFace-FaceNet

CSDN : friklogff
"""
# from imutils.video import VideoStream
# import cv2
# import imutils
#
# def main(capture_frame_count):
#     vs = VideoStream(src=0).start()  # 打开默认摄像头
#
#     frame_count = 0
#
#     while True:
#         frame = vs.read()  # 读取一帧图像
#
#         # 显示图像
#         cv2.imshow('Camera', frame)
#
#         key = cv2.waitKey(1)
#
#         if key == 32:  # 如果按下空格键，拍照
#             # 保存图像
#             cv2.imwrite(f'photo_{frame_count}.jpg', frame)
#             frame_count += 1
#
#
#         if key == 27:  # 如果按下ESC键，退出循环
#             break
#
#     # 释放摄像头和销毁窗口
#     vs.stop()
#     cv2.destroyAllWindows()
#
# if __name__ == "__main__":
#     capture_frame_count = 0
#     main(capture_frame_count)
from imutils.video import VideoStream
import cv2

# 创建VideoStream对象并使用FileVideoStream初始化

# 为了让FileVideoStream启动，请稍等片刻
import time
time.sleep(2.0)
vs = VideoStream(src='R.mp4').start()

while True:
    frame = vs.read()

    if frame is None:
        break  # 视频已经结束

    cv2.imshow("Frame", frame)

    if cv2.waitKey(1) & 0xFF == 27:  # 按下ESC键退出
        break

vs.stop()
cv2.destroyAllWindows()
