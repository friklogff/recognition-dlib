"""

NAME : gui_tk_test

USER : admin

DATE : 10/10/2023

PROJECT_NAME : RetinaFace-FaceNet

CSDN : friklogff
"""
import cv2
from PIL import Image, ImageTk
import tkinter as tk
import try_7

# # 创建FaceDetection对象
# detector = try_7.FaceDetection('R.mp4')
#
# # 新增全局变量
# capture_active = True
#
# def imshow():
#     global detector
#     global root
#     global image
#     global capture_active
#
#     if not capture_active:
#         return
#
#     res, img = detector.process_frame()
#
#     if res:
#         flag = detector.get_flag()
#
#         # 在这里获取帧和用户名
#         ref,frame = detector.process_frame()
#         username = detector.get_name()
#
#         if flag == 1:
#             # 插入签到信息到数据库
#             print(flag)
#             cv2.imwrite("last_frame.png", frame)
#             capture_active = False
#
#         img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#         img = Image.fromarray(img)
#         img = ImageTk.PhotoImage(img)
#         image.img = img
#         image['image'] = img
#
#     root.after(10, imshow)
#
# def quit_app():
#     global root
#     global capture_active
#     capture_active = False  # 设置捕获为非活跃状态
#     root.quit()
#
# root = tk.Tk()
# root.geometry("640x480")
# root.resizable(False, False)
# root.title('video')
#
# quit_button = tk.Button(root, text="退出", command=quit_app)
# quit_button.pack()
#
# image = tk.Label(root, text=' ', width=640, height=480)
# image.place(x=0, y=0, width=640, height=480)
#
# imshow()
#
# root.mainloop()
#
# # 不要忘记释放video资源
# detector.cap.release()

import tkinter as tk
import cv2
from PIL import Image, ImageTk


class OpenCVApp:
    def __init__(self, root, video_source=0):
        self.root = root
        self.root.title("OpenCV Integration")

        self.video_source = video_source
        self.cap = try_7.FaceDetection('R.mp4')

        self.canvas = tk.Canvas(root, width=self.cap.get(3), height=self.cap.get(4))
        self.canvas.pack()

        self.capture_active = True  # 控制视频捕获是否活跃

        # 创建“停止”按钮
        self.stop_button = tk.Button(root, text="停止视频捕获", command=self.stop_capture)
        self.stop_button.pack()

        self.update()

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def update(self):
        while self.capture_active:
            ret, frame = self.cap.process_frame()
            # ret, frame = self.cap.read()
            if ret:
                self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
                self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
                self.root.update()  # 更新Tkinter界面
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break  # 如果没有帧可读取，退出循环

    def stop_capture(self):
        self.capture_active = False  # 停止视频捕获

    def on_closing(self):
        self.cap.release()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = OpenCVApp(root)
    root.mainloop()
