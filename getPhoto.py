import cv2 as cv2
import numpy as np

capture = cv2.VideoCapture(0)
index = 1
while True:
    ret, frame = capture.read()
    if ret is True:
        cv2.imshow("frame", frame)
        index += 1
        if index % 5 == 0:
            cv2.imwrite("./king/" + str(index) + ".jpg", frame)
        c = cv2.waitKey(50)
        if c == 27: # ESC
            break
    else:
        break

cv2.destroyAllWindows()