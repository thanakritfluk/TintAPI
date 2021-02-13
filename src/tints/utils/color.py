import numpy as np
import os
from os.path import join as pjoin
import PIL.Image as Image
import colorsys
from colormath.color_objects import LabColor
from colormath.color_diff import delta_e_cie2000
from src.tints.utils.converter import rgb2lab
from colorthief import ColorThief
from src.tints.utils.kmean import get_colors

# Contain dominant color function ot any function to compare between 2 colors
def compare_delta_e (mean_color,RGB_tuple):
    # convert RGB to lab color space for put in an comparison formula which is delta e cie2000
    lab1 = rgb2lab(RGB_tuple[0],RGB_tuple[1],RGB_tuple[2])
    lab2 = rgb2lab(mean_color[0], mean_color[1] , mean_color[2])

    # create color from lab value
    # Reference color.
    color1 = LabColor(lab_l=lab1[0], lab_a=lab1[1], lab_b=lab1[2])
    # Color to be compared to the reference.
    color2 = LabColor(lab_l=lab2[0], lab_a=lab2[1], lab_b=lab2[2])
    # This is your delta E value as a float.
    delta_e = delta_e_cie2000(color1, color2, Kl=1, Kc=1, Kh=1)
    return float(format(delta_e,".3f"))

# Mean of the color in crop image
def load_color(dir,list):
    count = 0
    for sub_dir in os.listdir(dir):  
        if sub_dir == 'output.txt':
            continue
        else:
            img_dir = pjoin(dir, sub_dir)  
            image = Image.open(img_dir)
            image = image.convert('RGB')
            # By color thief
            # dmc= get_dominant_color_thief(image,img_dir)
            # By kmean
            dmc= get_dominant_color_kmean(image,img_dir)
            list.append(dmc)
            count = count+1
    return count

def get_mean_color(count,color_list):
    Mean_R=Mean_G=Mean_B=0
    for i in range(count):
        tuple=color_list[i]
        Mean_R+=tuple[0]
        Mean_G+=tuple[1]
        Mean_B+=tuple[2]
    MeanC=((int)(Mean_R/count),(int)(Mean_G/count),(int)(Mean_B/count))
    return MeanC    

# Dominant color in image
# Method 1 play with COLOR FORMAT
def get_dominant(image, image_path):
    max_score = 0.0
    dmc = None #dmc stand for dominant color
    for count,(r,g,b) in image.getcolors(image.size[0]*image.size[1]):
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

# Method 2 using lib color-thief implement of median cut
def get_dominant_color_thief(image, image_path):
    color_thief = ColorThief(image_path)
    # get the dominant color
    dominant_color = color_thief.get_color(quality=1)
    print(dominant_color)
    # build a color palette
    palette = color_thief.get_palette(color_count=3)
    print(palette)
    return dominant_color

# Method 3 using K-mean 5 platte
def get_dominant_color_kmean(image, image_path):
    dominant_color = get_colors(image_path)
    return dominant_color