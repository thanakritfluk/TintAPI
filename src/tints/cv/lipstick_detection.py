import cv2
import dlib
import numpy as np
import colorsys
from PIL import ImageColor
from src.tints.utils.color import compare_delta_e,load_color, get_mean_color
from os.path import join as pjoin
from src.tints.cv.detector import face_detect
from src.tints.models.lipstick import Lipstick
from src.tints.settings import APP_INPUT,APP_OUTPUT,SHAPE_68_PATH, COLOR_COMPARE_VAL

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
               #  print(pt_pos)
                # cv2.circle(detect[1], pt_pos, 2, (255, 0, 0), 1)
                np_pos[i-56][0] = pt.x
                np_pos[i-56][1] = pt.y
    cv2.imwrite(pjoin( APP_INPUT,"LanmarkPoint.jpg"), lanmark_img)    
    lip_point = np.array(lip_point)
    crop_lip = createBox(detect[1], lip_point[0:len(lip_point)+1])
    cv2.imwrite(pjoin( APP_OUTPUT,"LipArea.jpg"), crop_lip)    
    return np_pos


def find_mean_color():
    color_list = []
    # img_dir = "./image/output"
    count = load_color(APP_OUTPUT,color_list)
    mean_color = get_mean_color(count,color_list)
    hsv_mean = colorsys.rgb_to_hsv(mean_color[0]/255.0, mean_color[1]/255.0, mean_color[2]/255.0)
    hsv_temp = tuple([100.0*x for x in hsv_mean])
    if hsv_temp[2] < 30:
        h = (hsv_temp[0]+20)
        s = (hsv_temp[1]+20)
        v = (hsv_temp[2]+20)
        print("equalized hsv:",h,s,v)
        hsv_converted = (h,s,v)
        hsv_converted = tuple([x/100.0 for x in hsv_converted])
        print("converted hsv:",hsv_converted)
        mean_color = tuple(round(i * 255) for i in colorsys.hsv_to_rgb(hsv_converted[0],hsv_converted[1],hsv_converted[2]))
    return mean_color

def get_lipstick (mean_color, brand_list):
    similar_lipstick = [] # for append similar lipstick
    for brand_name in brand_list:
        lipstick_list = Lipstick.find_lipstick_by_brand(brand_name)
        # series_len = len(lipstick_list)
        # print(brand_name," have serie length =",series_len)
        for serie in lipstick_list:
            # print(serie_name,"Serie have color",serie['product_colors'])
            for color in serie['product_colors']:
               rgb_color = ImageColor.getcolor(color['hex_value'], "RGB")
               str_rgb_color = str(rgb_color)
               compare_result = compare_delta_e(mean_color, rgb_color)
               if(compare_result <= COLOR_COMPARE_VAL):
                    similar_lipstick.append({'_id':serie['_id'],'brand':brand_name,'price':serie['price'],'image_link':serie['image_link'],'product_link':serie['product_link'],'category':serie['category'],'color_name':color['colour_name'],'rgb_value':str_rgb_color, 'deltaE':compare_result, 'api_image_link': serie['api_featured_image']})
    return similar_lipstick

def predict_lipstick_color(ref_img):    
    data =  face_detect(ref_img)
    lip_np_pos = detect_mouth_np_array(data)
    # crop(data[1],lip_np_pos)
    meancolor = find_mean_color()
    print("Mean color=",meancolor)
    brand_list = Lipstick.distinct_brand()
    # print("Brand list=",brand_list)
    return get_lipstick(meancolor, brand_list)

# if __name__ == "__main__":
#     predict_lipstick_color()