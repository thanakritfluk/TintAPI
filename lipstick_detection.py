import cv2
import os
import dlib
import numpy as np
import colorsys
import PIL.Image as Image
from utils.color_similarity import compare_delta_e
from os.path import join as pjoin
from detector import face_detect

# Contain all lipstick detect function


def get_dominant(img):
    max_score = 0.0
    dmc = None #dmc stand for dominant color
    for count,(r,g,b) in img.getColor(img.size[0]*img.size[1]):
        # convert rgb to hsv
        saturation = colorsys.rgb_to_hsv(r/255.0, g/255.0, b/255.0)[1]
        # calculate y from yuv, y is represent the brightness or luminance of that pixels
        y = min(abs(r*2104+g*4130+b*802+4096+131072)>>13,235)
        # rescaling to y' which the value is in range of [0,1]
        y = (y-16.0)/(235-16)

        # remove pixels that has too high brightness
        if y > 0.9:
            continue
        # +0.1 since we still want the dark pixels to conpare
        score = (saturation+0.1)*count
        
        if score > max_score:
            max_score = score
            dmc = (r,b,g)
    return dmc

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

def load_color(dir,list):
    count = 0
    for sub_dir in os.listdir(dir):  
        img_dir = pjoin(dir, sub_dir)  
        image = Image.open(img_dir)
        image = image.convert('RGB')
        dmc=get_dominant(image)
        list.append(dmc)
        count = count+1
    return count

def get_mean_color(count,color_list):
    Mean_R=Mean_G=Mean_B=0
    for i in range(count):
        tuple=list[i]
        Mean_R+=tuple[0]
        Mean_G+=tuple[1]
        Mean_B+=tuple[2]
    MeanC=((int)(Mean_R/count),(int)(Mean_G/count),(int)(Mean_B/count))
    return MeanC

def find_mean_color():
    color_list = []
    img_dir = "./image/output"
    count = load_color(img_dir,color_list)
    mean_color = get_mean_color(count,color_list)
    return mean_color

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

def get_lipstick (mean_color):
    similar_lipstick = [] # for append similar lipstick
    # TODO: operate data from database or whatever which need all of lipstick
    # TODO: Compare color call function: compare_delta_e
    # TODO: If delta_e is in range [0,20] add to similar_lipstick
    return similar_lipstick


# if __name__ == "__main__":
#     img = cv2.imread("../img.jpg")
#     print(face_detect(img))