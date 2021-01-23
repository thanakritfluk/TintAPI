import cv2
import dlib
import numpy as np
from detector import face_detect

# Contain all lipstick detect function

def detect_mouth_np_array(detect):
    np_pos = np.zeros((3, 2), dtype=int)
    # Define feature predictor
    predictor = dlib.shape_predictor('./shape_predictor_68_face_landmarks.dat')
    for index, face in enumerate(detect[0]):
        shape = predictor(detect[2], face)
        for i, pt in enumerate(shape.parts()):
            pt_pos = (pt.x, pt.y)
            if i >= 48 and i <= 67:
                cv2.circle(detect[1], pt_pos, 2, (255, 0, 0), 1)
            if i >= 56 and i <= 58:
               #  print(pt_pos)
                cv2.circle(detect[1], pt_pos, 2, (255, 0, 0), 1)
                np_pos[i-56][0] = pt.x
                np_pos[i-56][1] = pt.y
    cv2.imwrite("./image/input/draw_lip.jpg", detect[1])    
    return np_pos


def crop(source,pos):

      x1=pos[2][0]
      y1=pos[2][1]
      x2=pos[1][0]
      y2=pos[1][1]
      d=abs(x2-x1)
      region = source[(int)(y1 - d * 0.75) :y2, x1:x2]
      # save the image
      cv2.imwrite("./image/output/Mouth1.jpg", region)
      
      x1=pos[1][0]
      y1=pos[1][1]
      x2=pos[0][0]
      y2=pos[0][1]
      d=abs(x1-x2)
      region = source[y1 - d :y2, x1:x2]
      # save the image
      cv2.imwrite("./image/output/Mouth2.jpg", region)


def predict_lipstick_color(ref_img):
    data =  face_detect(ref_img)
    lip_np_pos = detect_mouth_np_array(data)
    crop(data[1],lip_np_pos)

# if __name__ == "__main__":
#     img = cv2.imread("../img.jpg")
#     print(face_detect(img))

