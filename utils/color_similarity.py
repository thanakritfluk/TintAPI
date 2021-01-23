from colormath.color_objects import LabColor
from colormath.color_diff import delta_e_cie2000
from utils.converter import rgb2lab
# Contain dominant color function ot any function to compare between 2 colors
def compare_delta_e (mean_color,RGB_array):
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