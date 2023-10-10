"""

NAME : detect

USER : admin

DATE : 10/10/2023

PROJECT_NAME : RetinaFace-FaceNet

CSDN : friklogff
"""
import cv2
import time
import pymsp


def check(names, conn):
    cam = cv2.VideoCapture(0)
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('face_trainer/trainer.yml')
    cascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascadePath)
    font = cv2.FONT_HERSHEY_SIMPLEX
    minW = 0.1 * cam.get(3)
    minH = 0.1 * cam.get(4)

    while True:
        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(int(minW), int(minH))
        )

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            idnum, confidence = recognizer.predict(gray[y:y + h, x:x + w])

            if confidence < 100:
                username = names[idnum - 1]
                confidence = "{0}%".format(round(100 - confidence))

                cv2.putText(img, str(username), (x + 5, y - 5), font, 1, (0, 0, 255), 1)
                cv2.putText(img, str(confidence), (x + 5, y + h - 5), font, 1, (0, 0, 0), 1)
                cv2.imshow('camera', img)
                time.sleep(2)

                db.record().insert_record(username, conn)  # 签到信息插入数据库
                cam.release()
                cv2.destroyAllWindows()
                return
            else:
                idnum = "unknown"
                confidence = "{0}%".format(round(100 - confidence))
                cv2.putText(img, str(idnum), (x + 5, y - 5), font, 1, (0, 0, 255), 1)
                cv2.putText(img, str(confidence), (x + 5, y + h - 5), font, 1, (0, 0, 0), 1)

        cv2.imshow('camera', img)
        k = cv2.waitKey(10)
        if k == 27:
            break

    cam.release()
    cv2.destroyAllWindows()
