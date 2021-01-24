import cv2
import dlib
import numpy as np


# Detect face position return array face array
def face_detect(img):
    img = cv2.imdecode(np.fromstring(img.read(), np.uint8), cv2.IMREAD_UNCHANGED)
    # print("Read image array =", img)
    image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    grayImg = cv2.equalizeHist(image)
    # Load detector from dlib
    detector = dlib.get_frontal_face_detector()
    # Use detector detect face position
    rectangle_position = detector(img, 1)
    cv2.imwrite("./image/input/source.jpg", img)
    for a in rectangle_position:
        cv2.rectangle(img, (a.left(), a.top()),
                      (a.right(), a.bottom()), (204, 0, 204))
    cv2.imwrite("./image/input/draw_rectangle.jpg", img)
    return rectangle_position, img, grayImg


# if __name__ == "__main__":
#     img = cv2.imread("../img.jpg")
#     print(face_detect(img))
