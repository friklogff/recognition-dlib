import tkinter as tk
import cv2
from PIL import Image, ImageTk
import os

class PhotoCaptureApp:
    def __init__(self, root, video_source=0):
        self.root = root
        self.root.title("拍照程序")

        self.video_source = video_source
        self.cap = cv2.VideoCapture(self.video_source)

        self.canvas = tk.Canvas(root, width=self.cap.get(3), height=self.cap.get(4))
        self.canvas.pack()

        # 创建输入框用于输入姓名
        self.name_entry = tk.Entry(root, width=30)
        self.name_entry.pack(pady=5)

        # 创建“拍照”按钮
        self.capture_button = tk.Button(root, text="拍照", command=self.capture_photo)
        self.capture_button.pack(pady=10)

        self.photo = None  # 存储捕获的图像
        self.photo_count = 1  # 图像计数，从1开始

    def capture_photo(self):
        ret, frame = self.cap.read()
        if ret:
            name = self.name_entry.get().strip()
            if not name:
                name = "Unknown"

            filename = f"{name}_{self.photo_count}.png"
            cv2.imwrite(filename, frame)
            print(f"Image captured and saved as '{filename}'.")
            self.photo_count += 1

    def update(self):
        ret, frame = self.cap.read()
        if ret:
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        self.root.after(10, self.update)

    def on_closing(self):
        self.cap.release()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = PhotoCaptureApp(root)
    app.update()
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
