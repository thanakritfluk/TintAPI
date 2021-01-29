import numpy as np
from colormath.color_objects import LabColor
from colormath.color_diff import delta_e_cie2000
from src.tints.utils.converter import rgb2lab

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
