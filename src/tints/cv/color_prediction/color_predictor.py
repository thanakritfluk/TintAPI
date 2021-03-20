import cv2
import numpy as np
from PIL import ImageColor
from src.tints.models.lipstick import Lipstick
from src.tints.cv.detector import DetectLandmarks
from src.tints.utils.color import compare_delta_e,get_dominant_color
from src.tints.settings import COLOR_PREDICTION_INPUT,COLOR_PREDICTION_OUTPUT, COLOR_COMPARE_VAL, METHOD_NUM, RETURN_SIZE



class ColorPredictor(DetectLandmarks):

    def __init__(self):
        """ Initiator method for class """
        DetectLandmarks.__init__(self)
        self.image = 0
        self.width = 0
        self.height = 0
        self.im_copy = 0
        self.height = 0
        self.width = 0
        self.user_id = 0
        

    def read_image(self, image, user_id):
        """ Read image from path forwarded """
        # self.image = cv2.imread(filename)
        self.image = cv2.imdecode(np.fromstring(image.read(), np.uint8), cv2.IMREAD_COLOR)
        # self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        self.im_copy = self.image.copy()
        self.height, self.width = self.image.shape[:2]
        self.user_id = user_id
        # print("Self predict =",self.predictor)
        # print("IMAGE =", self.image)
    
    def print_result(self,number, product_list):
        print()
        if(len(product_list) <= number):
            for i in range(len(product_list)):
                print("Brand = {}, Color name = {}, RGB = {}, DeltaE = {}".format(product_list[i]["brand"],product_list[i]["color_name"],product_list[i]["rgb_value"], product_list[i]["deltaE"]))
        else:
            for i in range(number):
                print("Brand = {}, Color name = {}, RGB = {}, DeltaE = {}".format(product_list[i]["brand"],product_list[i]["color_name"],product_list[i]["rgb_value"], product_list[i]["deltaE"]))
        print()



    def get_lipstick_predict(self):
        lip_np = self.get_lip_np(self.image)
        LIPAREA_NAME = "".join(("LipArea_",self.user_id,".jpg"))
        self.create_box(self.image,COLOR_PREDICTION_OUTPUT,LIPAREA_NAME,lip_np)
        # Find lipstick after get crop area
        brand_list = Lipstick.distinct_brand()
        dominant_color_list = get_dominant_color(COLOR_PREDICTION_OUTPUT, self.user_id)
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
            if not similar_lipstick:
                break
        if len(similar_lipstick) >= RETURN_SIZE:
            similar_lipstick = similar_lipstick[:RETURN_SIZE]
        else:
            similar_lipstick = similar_lipstick[:len(similar_lipstick)]
        similar_lipstick.sort(key=lambda x: x.get('deltaE'))
        # Print for check return lip color easeier
        self.print_result(5,similar_lipstick)
        return similar_lipstick

    def get_foundation_predict(self):
        pass
        #  if i>=2 and i<=5 or i ==29  or i== 40 or i ==49:
        #  cheek_point.append([pt.x,pt.y])    


