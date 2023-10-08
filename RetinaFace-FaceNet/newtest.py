from imutils.video import FileVideoStream
from imutils.video import VideoStream
from imutils import face_utils
import numpy as np
import imutils
import dlib
import cv2
import sys


def _help():
    print("Usage:")
    print("     python mouth_open_detect.py")
    print("     python mouth_open_detect.py <path of a video>")
    print("For example:")
    print("     python mouth_open_detect.py video/lee.mp4")
    print("If the path of a video is not provided, the camera will be used as the input.Press q to quit.")


def mouth_aspect_ratio(mouth):
    A = np.linalg.norm(mouth[2] - mouth[9])  # 51, 59
    B = np.linalg.norm(mouth[4] - mouth[7])  # 53, 57
    C = np.linalg.norm(mouth[0] - mouth[6])  # 49, 55
    mar = (A + B) / (2.0 * C)

    return mar


def mouth_open_detection(vs, file_stream):
    MAR_THRESH = 0.5

    print("[INFO] loading facial landmark predictor...")
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("model/shape_predictor_68_face_landmarks.dat")

    (mStart, mEnd) = face_utils.FACIAL_LANDMARKS_IDXS["mouth"]

    print("[INFO] starting video stream thread...")
    while True:
        if file_stream and not vs.more():
            break
        frame = vs.read()
        if frame is not None:
            frame = imutils.resize(frame, width=450)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            rects = detector(gray, 0)

            for rect in rects:
                shape = predictor(gray, rect)
                shape = face_utils.shape_to_np(shape)

                mouth = shape[mStart:mEnd]
                mar = mouth_aspect_ratio(mouth)

                mouth_hull = cv2.convexHull(mouth)
                cv2.drawContours(frame, [mouth_hull], -1, (0, 255, 0), 1)

                if mar > MAR_THRESH:
                    cv2.putText(frame, "Mouth is open!", (10, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

                cv2.putText(frame, "MAR: {:.2f}".format(mar), (300, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

            cv2.imshow("Frame", frame)
            key = cv2.waitKey(1) & 0xFF

            if key == ord("q"):
                break

    cv2.destroyAllWindows()
    vs.stop()


if len(sys.argv) > 2 or "-h" in sys.argv or "--help" in sys.argv:
    _help()
elif len(sys.argv) == 2:
    vs = FileVideoStream(sys.argv[1]).start()
    file_stream = True
    mouth_open_detection(vs, file_stream)
else:
    vs = VideoStream(src=0).start()
    file_stream = False
    mouth_open_detection(vs, file_stream)