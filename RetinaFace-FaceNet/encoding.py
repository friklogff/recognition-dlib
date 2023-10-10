# import os
#
# from retinaface import Retinaface
#
# '''
# 在更换facenet网络后一定要重新进行人脸编码，运行encoding.py。
# '''
# retinaface = Retinaface(1)
#
# list_dir = os.listdir("face_dataset")
# image_paths = []
# names = []
# for name in list_dir:
#     image_paths.append("face_dataset/"+name)
#     print(names,image_paths)
#     names.append(name.split("_")[0])
#
# retinaface.encode_face_dataset(image_paths,names)
import numpy as np

# 指定.npy文件的路径
file_path = "model_data/mobilenet_names.npy"
# file_path = "model_data/mobilenet_face_encoding.npy"

# 使用NumPy的load方法加载.npy文件
data = np.load(file_path)
print(data)