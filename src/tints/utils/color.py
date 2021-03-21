import numpy as np
import os
from os.path import join as pjoin
import PIL.Image as Image
import colorsys
from colormath.color_objects import LabColor
from colormath.color_diff import delta_e_cie2000
from src.tints.utils.converter import rgb2lab
from src.tints.utils.kmean import get_colors
from src.tints.settings import BLACK_THRESHOLD

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

def load_image(userID,dir):
    for sub_dir in os.listdir(dir):  
        if userID in sub_dir:
            img_dir = pjoin(dir, sub_dir)  
            image = Image.open(img_dir)
            image = image.convert('RGB')
    return image,img_dir


# Method 3 using K-mean 5 platte
def get_dominant_color_kmean(image_path):
    dominant_color = get_colors(image_path)
    return dominant_color


def get_dominant_color(dir_folder, userID):
    img_info = load_image(userID,dir_folder)
    dominant_color_list = []
    dominant_color_list = get_dominant_color_kmean(img_info[1])
    return dominant_color_list