import cv2
import pickle
import numpy as np
from PIL import ImageColor
from os.path import join as pjoin
from src.tints.models.lipstick import Lipstick
from src.tints.models.foundation import Foundation
from src.tints.models.blush import Blush
from src.tints.cv.detector import DetectLandmarks
from src.tints.utils.color import compare_delta_e,get_dominant_color_kmean
from src.tints.settings import COLOR_PREDICTION_INPUT,COLOR_PREDICTION_OUTPUT, COLOR_COMPARE_VAL, METHOD_NUM, RETURN_SIZE,SKIN_CLUSTER_MODEL_PATH

SKIN_CLUSTER_MODEL = SKIN_CLUSTER_MODEL_PATH

class ColorPredictor(DetectLandmarks):

    def __init__(self,ref_image, user_id):
        """ Initiator method for class """
        DetectLandmarks.__init__(self)
        self.image = self.read_image(ref_image)
        self.user_id = user_id
        

    def read_image(self,image):
        """ Read image from path forwarded """
        return cv2.imdecode(np.fromstring(image.read(), np.uint8), cv2.IMREAD_COLOR)
    
    def print_result(self,number, product_list):
        print()
        if(len(product_list) <= number):
            for i in range(len(product_list)):
                print("Brand = {}, Color name = {}, RGB = {}, DeltaE = {}".format(product_list[i]["brand"],product_list[i]["color_name"],product_list[i]["rgb_value"], product_list[i]["deltaE"]))
        else:
            for i in range(number):
                print("Brand = {}, Color name = {}, RGB = {}, DeltaE = {}".format(product_list[i]["brand"],product_list[i]["color_name"],product_list[i]["rgb_value"], product_list[i]["deltaE"]))
        print()

    def get_custom_return_size(self,lst):
        result = []
        if len(lst) >= RETURN_SIZE:
            result = lst[:RETURN_SIZE]
        else:
            result = lst[:len(lst)]
        result.sort(key=lambda x: x.get('deltaE'))
        return result



    def get_lipstick_predict(self):
        lip_np = self.get_lip_np(self.image)
        LIPAREA_NAME = "".join(("LipArea_",self.user_id,".jpg"))
        self.create_box(self.image,COLOR_PREDICTION_OUTPUT,LIPAREA_NAME,lip_np)
        # Find lipstick after get crop area
        brand_list = Lipstick.distinct_brand()
        img_path = pjoin(COLOR_PREDICTION_OUTPUT,LIPAREA_NAME)
        dominant_color_list = get_dominant_color_kmean(img_path)
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
                                similar_lipstick.append({'_id':serie['_id'],'brand':brand_name,'serie':serie['name'],'price':serie['price'],'image_link':serie['image_link'],'product_link':serie['product_link'],'category':serie['category'],'color_name':color['colour_name'],'rgb_value':str_rgb_color, 'deltaE':compare_result, 'api_image_link': serie['api_featured_image']})
            if similar_lipstick:
                break
        # Print for check return lip color easeier
        self.print_result(5,similar_lipstick)
        return self.get_custom_return_size(similar_lipstick)


    def get_skin_type_cluster(self, rgb):
        """ 
        Return skin type divied in 4 category:
        - 0 Light
        - 1 Medium
        - 2 Fair
        - 3 Tan
        """
        load_model = pickle.load(open(SKIN_CLUSTER_MODEL,'rb'))
        skin_type = load_model.predict([rgb])
        return int(skin_type)

    def get_foundation_predict(self):
        cheek_np = self.get_cheek_np(self.image)
        CHEEK_NAME = "".join(("CheekArea_",self.user_id,".jpg"))
        self.create_box(self.image, COLOR_PREDICTION_OUTPUT, CHEEK_NAME, cheek_np)
        img_path = pjoin(COLOR_PREDICTION_OUTPUT,CHEEK_NAME)
        dominant_color_list = get_dominant_color_kmean(img_path)
        similar_foundation = []
        foundation_list = []
        for dominant_color in dominant_color_list:
            skin_cluster = self.get_skin_type_cluster(dominant_color)
            if not foundation_list: 
                foundation_list = Foundation.get_foundation_by_skin_cluster(skin_cluster)
            for foundation in foundation_list:
                rgb_color = ImageColor.getcolor(foundation['product_color']['hex_value'], "RGB")
                str_rgb_color = str(rgb_color)
                compare_result = compare_delta_e(dominant_color, rgb_color)
                print(rgb_color)
                if(compare_result <= COLOR_COMPARE_VAL):
                    similar_foundation.append({'_id':foundation['_id'],'brand':foundation['brand'],'serie':foundation['name'],'price':foundation['price'],'price_sign':foundation['price_sign'],'currency':foundation['currency'],'image_link':foundation['image_link'],'product_link':foundation['product_link'],'category':foundation['category'],'color_name':foundation['product_color']['colour_name'],'rgb_value':str_rgb_color, 'deltaE':compare_result, 'api_image_link': foundation['api_featured_image']})
            if similar_foundation:
                break
        self.print_result(5,similar_foundation)
        return self.get_custom_return_size(similar_foundation)
        
        #  if i>=2 and i<=5 or i ==29  or i== 40 or i ==49:
        #  cheek_point.append([pt.x,pt.y])    

    def get_cheek_predict(self):
        pass

