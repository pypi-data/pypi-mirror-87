import numpy as np
import cv2 as cv
import json
import os

class MLVideo():
    def __init__(self, videopath):
        self.videopath = videopath

    def getvideo(self):
        return cv.VideoCapture(self.videopath)

    def videotoarray(self, capture, savepath="video.json"):
        success = 1
        while success:
            success, image = capture.read()
            with open(savepath, 'a') as f:
                json.dump(np.asarray(image).tolist(), f)
                f.write(os.linesep)

# cap = cv.VideoCapture('C:/Users/bugsi/PycharmProjects/MLPlus/videoplayback.mp4')
# while cap.isOpened():
#     ret, frame = cap.read()
#     # if frame is read correctly ret is True
#     if not ret:
#         print("Can't receive frame (stream end?). Exiting ...")
#         break
#     gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
#     cv.imshow('frame', gray)
#     print(np.asarray(gray))
#     if cv.waitKey(1) == ord('q'):
#         break
# cap.release()
# cv.destroyAllWindows()