import cv2
import os
import dlib
import numpy as np
import colorsys
import PIL.Image as Image
from colormath.color_objects import LabColor
from colormath.color_diff import delta_e_cie2000
from os.path import join as pjoin
from detector import face_detect

# Contain all lipstick detect function

# Method for converting RGB color space to LAB color space
def rgb2lab(R,G,B):
    # Convert RGB to XYZ
    var_R = ( R / 255.0 )        # R from 0 to 255
    var_G = ( G / 255.0 )        # G from 0 to 255
    var_B = ( B / 255.0 )        # B from 0 to 255

    if ( var_R > 0.04045 ): 
        var_R = ( ( var_R + 0.055 ) / 1.055 ) ** 2.4
    else:                   
        var_R = var_R / 12.92
    if ( var_G > 0.04045 ): 
        var_G = ( ( var_G + 0.055 ) / 1.055 ) ** 2.4
    else:                   
        var_G = var_G / 12.92
    if ( var_B > 0.04045 ): 
        var_B = ( ( var_B + 0.055 ) / 1.055 ) ** 2.4
    else:                   
        var_B = var_B / 12.92

    var_R = var_R * 100.0
    var_G = var_G * 100.0
    var_B = var_B * 100.0

    # Observer. = 2°, Illuminant = D65
    X = var_R * 0.4124 + var_G * 0.3576 + var_B * 0.1805
    Y = var_R * 0.2126 + var_G * 0.7152 + var_B * 0.0722
    Z = var_R * 0.0193 + var_G * 0.1192 + var_B * 0.9505
    
    # Convert XYZ to L*a*b*
    var_X = X / 95.047         # ref_X =  95.047   Observer= 2°, Illuminant= D65
    var_Y = Y / 100.000        # ref_Y = 100.000
    var_Z = Z / 108.883        # ref_Z = 108.883

    if ( var_X > 0.008856 ): 
        var_X = var_X ** ( 1.0/3.0 )
    else:                    
        var_X = ( 7.787 * var_X ) + ( 16.0 / 116.0 )
    if ( var_Y > 0.008856 ): 
        var_Y = var_Y ** ( 1.0/3.0 )
    else:
        var_Y = ( 7.787 * var_Y ) + ( 16.0 / 116.0 )
    if ( var_Z > 0.008856 ): 
        var_Z = var_Z ** ( 1.0/3.0 )
    else:                    
        var_Z = ( 7.787 * var_Z ) + ( 16.0 / 116.0 )

    CIE_L = ( 116.0 * var_Y ) - 16.0
    CIE_a = 500.0 * ( var_X - var_Y )
    CIE_b = 200.0 * ( var_Y - var_Z )
    return (CIE_L, CIE_a, CIE_b)

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

def compare_delta_e (mean_color):
    # TODO: operate data from database or whatever which need all of lipstick
    sum = 0 # TODO: sum = amount of color in database
    RGB_array = np.zeros((sum,3), dtype=int) #TODO: in RGB array must contain an [R G B] color separately
    DELTA_E_temp = np.zeros((sum,1), dtype=float)
    for i in range(sum):
        # take an R G B value from RGB array for each color
        R=RGB_array[i][0]
        G=RGB_array[i][1]
        B=RGB_array[i][2]
        
        # convert RGB to lab color space for put in an comparison formula which is delta e cie2000
        lab1 = rgb2lab(R,G,B)
        lab2 = rgb2lab(mean_color[0], mean_color[1] , mean_color[2])

        # create color from lab value
        # Reference color.
        color1 = LabColor(lab_l=lab1[0], lab_a=lab1[1], lab_b=lab1[2])
        # Color to be compared to the reference.
        color2 = LabColor(lab_l=lab2[0], lab_a=lab2[1], lab_b=lab2[2])
        # This is your delta E value as a float.
        DELTA_E_temp[i] = delta_e_cie2000(color1, color2, Kl=1, Kc=1, Kh=1)
    
    # sort index of delta_e by delta e value ASC
    result=sorted(range(len(DELTA_E_temp)), key=lambda k: DELTA_E_temp[k])
    top_three = []
    # append top 3 lipstick that has less difference
    for i in range(3):
        top_three.append(i) # TODO: add from lipsticl list
    return top_three


# if __name__ == "__main__":
#     img = cv2.imread("../img.jpg")
#     print(face_detect(img))