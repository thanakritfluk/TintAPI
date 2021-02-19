import cv2
import dlib
import numpy as np
import colorsys
from PIL import ImageColor
from src.tints.utils.color import compare_delta_e,get_dominant_color
from os.path import join as pjoin
from src.tints.cv.detector import face_detect
from src.tints.models.lipstick import Lipstick
from src.tints.settings import APP_INPUT,APP_OUTPUT,SHAPE_68_PATH, COLOR_COMPARE_VAL, METHOD_NUM

# Contain all lipstick detect function

def createBox(img, points, scale=1):
    mask = np.zeros_like(img)
    # Our feature
    mask = cv2.fillPoly(mask, [points], (255,255,255))
    # cv2.imwrite(pjoin( APP_OUTPUT,"LipMask.jpg"), mask)   
    img = cv2.bitwise_and(img,mask)
    # cv2.imwrite(pjoin( APP_OUTPUT,"OnlyLipIMG.jpg"), img)  
    bbox = cv2.boundingRect(points)
    x,y,w,h = bbox
    imgCrop = img[y:y+h, x:x+w]
    # imgCrop = cv2.resize(imgCrop, (0,0), None, scale, scale)
    return imgCrop

def detect_mouth_np_array(detect):
    np_pos = np.zeros((3, 2), dtype=int)
    # Define feature predictor
    predictor = dlib.shape_predictor(SHAPE_68_PATH)
    lip_point = []
    lanmark_img = np.copy(detect[1])
    for index, face in enumerate(detect[0],0):
        shape = predictor(detect[2], face)
        for i, pt in enumerate(shape.parts()):
            pt_pos = (pt.x, pt.y)
            cv2.circle(lanmark_img, pt_pos, 2, (255, 255, 255), 2)
            if i >= 48 and i <= 67:
                lip_point.append([pt.x,pt.y])
                # cv2.circle(detect[1], pt_pos, 2, (255, 0, 0), 1)
            if i >= 56 and i <= 58:
                # cv2.circle(detect[1], pt_pos, 2, (255, 0, 0), 1)
                np_pos[i-56][0] = pt.x
                np_pos[i-56][1] = pt.y
    cv2.imwrite(pjoin( APP_INPUT,"LanmarkPoint.jpg"), lanmark_img)    
    lip_point = np.array(lip_point)
    crop_lip = createBox(detect[1], lip_point[0:len(lip_point)+1])
    cv2.imwrite(pjoin( APP_OUTPUT,"LipArea.jpg"), crop_lip)


def find_dominant_color():
    dominant_list = get_dominant_color(METHOD_NUM,APP_OUTPUT)
    return dominant_list


def print_result(number, lip_list):
    print()
    if(len(lip_list) <= number):
        for i in range(len(lip_list)):
            print("Brand = {}, Color name = {}, RGB = {}, DeltaE = {}".format(lip_list[i]["brand"],lip_list[i]["color_name"],lip_list[i]["rgb_value"], lip_list[i]["deltaE"]))
    else:
        for i in range(number):
            print("Brand = {}, Color name = {}, RGB = {}, DeltaE = {}".format(lip_list[i]["brand"],lip_list[i]["color_name"],lip_list[i]["rgb_value"], lip_list[i]["deltaE"]))
    print()

def get_lipstick (dominant_color_list, brand_list):
    similar_lipstick = [] # for append similar lipstick
    for dominant_color in dominant_color_list:
        for brand_name in brand_list:
            lipstick_list = Lipstick.find_lipstick_by_brand(brand_name)
            for serie in lipstick_list:
                for color in serie['product_colors']:
                    rgb_color = ImageColor.getcolor(color['hex_value'], "RGB")
                    str_rgb_color = str(rgb_color)
                    # Compare using delta_e
                    compare_result = compare_delta_e(dominant_color, rgb_color)
                    if(compare_result <= COLOR_COMPARE_VAL):
                            similar_lipstick.append({'_id':serie['_id'],'brand':brand_name,'price':serie['price'],'image_link':serie['image_link'],'product_link':serie['product_link'],'category':serie['category'],'color_name':color['colour_name'],'rgb_value':str_rgb_color, 'deltaE':compare_result, 'api_image_link': serie['api_featured_image']})
        if not similar_lipstick:
            break
    similar_lipstick.sort(key=lambda x: x.get('deltaE'))
    # Print for check return lip color easeier
    print_result(5,similar_lipstick)
    return similar_lipstick

def predict_lipstick_color(ref_img):    
    data =  face_detect(ref_img)
    detect_mouth_np_array(data)
    dominant_color_list = find_dominant_color()
    print("Dominant color list=",dominant_color_list)
    brand_list = Lipstick.distinct_brand()
    return get_lipstick(dominant_color_list, brand_list)

# if __name__ == "__main__":
#     predict_lipstick_color()