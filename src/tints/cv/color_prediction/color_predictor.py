import cv2
import pickle
import numpy as np
# from PIL import Image
# from numpy import asarray
from PIL import ImageColor,Image
from os.path import join as pjoin
from src.tints.models.lipstick import Lipstick
from src.tints.models.foundation import Foundation
from src.tints.models.blush import Blush
from src.tints.cv.detector import DetectLandmarks
from src.tints.utils.color import compare_delta_e,get_dominant_color_kmean
from src.tints.settings import COLOR_PREDICTION_INPUT,COLOR_PREDICTION_OUTPUT, COLOR_COMPARE_VAL, METHOD_NUM, RETURN_SIZE,SKIN_CLUSTER_MODEL_PATH, SAVE_FILE_TYPE

SKIN_CLUSTER_MODEL = SKIN_CLUSTER_MODEL_PATH

class ColorPredictor(DetectLandmarks):

    def __init__(self, user_id=None, flag=None):
        """ Initiator method for class """
        DetectLandmarks.__init__(self)
        self.image = 0
        self.user_id = user_id
        self.flag = flag
        

    def read_image_from_request_file(self,image):
        """ Read image from path forwarded """
        self.image = cv2.imdecode(np.fromstring(image.read(), np.uint8), cv2.IMREAD_COLOR)

    def read_image_from_storage(self, filename):
        image_path = pjoin(COLOR_PREDICTION_INPUT,filename)
        self.image = image_path
 

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

    def get_prediction_list(self,similar_list, product_list, dominant_color):
        for product in product_list:
            for color in product['product_colors']:
                if "," in color['hex_value']:
                    color_list = color['hex_value'].split(",")
                    for i in color_list:
                        rgb_color = ImageColor.getcolor(i, "RGB")
                        str_rgb_color = str(rgb_color)
                        # Compare using delta_e
                        compare_result = compare_delta_e(dominant_color, rgb_color)
                        if(compare_result <= COLOR_COMPARE_VAL):
                                similar_list.append({'_id':product['_id'],'brand':product['brand'],'serie':product['name'],'price':product['price'],'image_link':product['image_link'],'product_link':product['product_link'],'category':product['category'],'color_name':color['colour_name'],'rgb_value':str_rgb_color, 'deltaE':compare_result, 'api_image_link': product['api_featured_image']})
                else:
                    rgb_color = ImageColor.getcolor(color['hex_value'], "RGB")
                    str_rgb_color = str(rgb_color)
                    # Compare using delta_e
                    compare_result = compare_delta_e(dominant_color, rgb_color)
                    if(compare_result <= COLOR_COMPARE_VAL):
                            similar_list.append({'_id':product['_id'],'brand':product['brand'],'serie':product['name'],'price':product['price'],'image_link':product['image_link'],'product_link':product['product_link'],'category':product['category'],'color_name':color['colour_name'],'rgb_value':str_rgb_color, 'deltaE':compare_result, 'api_image_link': product['api_featured_image']})
        return similar_list



    def get_lipstick_predict(self):
        lip_np = self.get_lip_np(self.image,self.flag)
        LIPAREA_NAME = "".join(("LipArea_",self.user_id))
        self.create_box(self.image,COLOR_PREDICTION_OUTPUT,LIPAREA_NAME,lip_np,self.flag)
        # Find lipstick after get crop area
        brand_list = Lipstick.distinct_brand()
        img_path = pjoin(COLOR_PREDICTION_OUTPUT,"".join((LIPAREA_NAME,SAVE_FILE_TYPE)))
        dominant_color_list = get_dominant_color_kmean(img_path)
        similar_lipstick = [] # for append similar lipstick
        for dominant_color in dominant_color_list:
            for brand_name in brand_list:
                lipstick_list = Lipstick.find_lipstick_by_brand(brand_name)
                similar_lipstick = self.get_prediction_list(similar_lipstick, lipstick_list, dominant_color)
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
        cheek_np = self.get_cheek_np(self.image, self.flag)        
        CHEEK_NAME = "".join(("CheekArea_",self.user_id))
        self.create_box(self.image, COLOR_PREDICTION_OUTPUT, CHEEK_NAME, cheek_np, self.flag)
        img_path = pjoin(COLOR_PREDICTION_OUTPUT,"".join((CHEEK_NAME,SAVE_FILE_TYPE)))
        dominant_color_list = get_dominant_color_kmean(img_path)
        similar_foundation = []
        foundation_list = []
        for dominant_color in dominant_color_list:
            skin_cluster = self.get_skin_type_cluster(dominant_color)
            if not foundation_list: 
                foundation_list = Foundation.get_foundation_by_skin_cluster(skin_cluster)
            similar_foundation = self.get_prediction_list(similar_foundation, foundation_list, dominant_color)
            if similar_foundation:
                break
        self.print_result(5,similar_foundation)
        return self.get_custom_return_size(similar_foundation)
        

    def get_blush_predict(self, blush_color):
        dominant_color = ImageColor.getcolor(blush_color, "RGB")
        similar_blush = []
        blush_list = Blush.get_all_blush()
        similar_blush = self.get_prediction_list(similar_blush, blush_list, dominant_color)
        # Print for check return lip color easeier
        self.print_result(5,similar_blush)
        return self.get_custom_return_size(similar_blush)


    def get_all_prediction(self,blush_color):
        self.save_localize_lanmark_image(self.image,COLOR_PREDICTION_INPUT,"".join(("Lanmark_",self.user_id)),self.flag)
        return {"Lipstick":self.get_lipstick_predict(),"Foundation":self.get_foundation_predict(),"Blush":self.get_blush_predict(blush_color)}
        

