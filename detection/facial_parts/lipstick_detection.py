import cv2
import dlib
import numpy as np

# Contain all lipstick detect function

def detect_mouth_np_array(detect, img):
    np_pos = np.zeros((3, 2), dtype=int)
    # Define feature predictor
    predictor = dlib.shape_predictor('../shape_predictor_68_face_landmarks.dat')
    for index, face in enumerate(detect[0]):
        shape = predictor(detect[1], face)
        for i, pt in enumerate(shape.parts()):
            print("")
            pt_pos = (pt.x, pt.y)
            if i >= 48 and i <= 67:
                cv2.circle(img, pt_pos, 2, (255, 0, 0), 1)
            if i >= 56 and i <= 58:
               #  print(pt_pos)
                cv2.circle(img, pt_pos, 2, (255, 0, 0), 1)
                np_pos[i-56][0] = pt.x
                np_pos[i-56][1] = pt.y
    return np_pos


# if __name__ == "__main__":
#     img = cv2.imread("../img.jpg")
#     print(face_detect(img))

