from PIL import ImageColor
from src.tints.cv.detector import DetectLandmarks
from src.tints.models.lipstick import Lipstick
from src.tints.models.foundation import Foundation
from src.tints.models.blush import Blush
from src.tints.models.user import User
from src.tints.settings import RECOMMENDATION_PATH, USER_IMAGE_PATH, SAVE_FILE_TYPE, USER_IMAGE_FILE_TYPE,SKIN_CLUSTER_MODEL_PATH
from src.tints.utils.color import compare_delta_e,get_dominant_color_kmean
from os.path import join as pjoin
from collections import Counter
import cv2
import pickle

class Recommendation(DetectLandmarks):

    
    def __init__(self,user_id):
        DetectLandmarks.__init__(self)
        self.user_id = user_id
        self.image = 0
    
    def set_image(self):
       image_path = "".join((self.user_id,USER_IMAGE_FILE_TYPE))
       self.image = cv2.imread(pjoin(USER_IMAGE_PATH,image_path))


    def get_skin_type_cluster(self, rgb):
        """ 
        Return skin type divied in 4 category:
        - 0 Light
        - 1 Medium
        - 2 Fair
        - 3 Tan
        """
        load_model = pickle.load(open(SKIN_CLUSTER_MODEL_PATH,'rb'))
        skin_type = load_model.predict([rgb])
        return int(skin_type)

    def get_skin_type(self, skin_type):
        if skin_type == 0:
            return "Light"
        elif skin_type == 1:
            return "Medium"
        elif skin_type == 2:
            return "Fair"
        else:
            return "Tan"


    def get_user_skin_type(self):
        cheek_np = self.get_cheek_np(self.image, "RECOMMENDATION_FILE_READ")
        CHEEK_NAME = "".join(("CheekArea_",self.user_id))
        self.create_box(self.image, RECOMMENDATION_PATH, CHEEK_NAME, cheek_np)
        img_path = pjoin(RECOMMENDATION_PATH,"".join((CHEEK_NAME,SAVE_FILE_TYPE)))
        dominant_color = get_dominant_color_kmean(img_path)[0]
        skin_type = self.get_skin_type_cluster(dominant_color)
        return self.get_skin_type(skin_type)

    
    def get_recommendation(self):
        self.set_image()
        # 1. สร้าง list เอาไว้เก็บ skin types
        # 2. เก็บสกินไทป์จากรูป user 
        # 3. check ว่า มี foundation ส่งมามั้ย 
            #   ถ้าไม่ ให้เอา skintype ที่ได้จาก รูป user ไปหา recommend เลย 
            #   ถ้ามี ให้เอา สี foundation ไปเข้า model หาสีผิว >> เก็บเข้า list >> Check majority vote นับ skintype ที่มากสุด จากใน list เอาไป recommend
        skin_type = self.get_user_skin_type()
        user = User(self.user_id)
        list_foundation = user.get_used_foundation()
        list_foundation = list_foundation[0]['foundationList']
        if list_foundation:
            list_skin_type = []
            list_skin_type.append(skin_type)
            list_skin_type.append("Medium")
            for selected in list_foundation:
                hex_value = selected['colorSelected']['hex_value']
                rgb_value = ImageColor.getcolor(hex_value, "RGB")
                list_skin_type.append(self.get_skin_type(self.get_skin_type_cluster(rgb_value)))
            list_skin_type = Counter(list_skin_type)
            skin_type = list_skin_type.most_common(1)[0][0]
            print("User skin type when compared with used foundation: {}".format(skin_type))
        blush_list = Blush.get_blush_by_skin_type(skin_type)
        lipstick_list = Lipstick.get_lipstick_by_skin_type(skin_type)
        foundation_list = Foundation.get_foundation_by_skin_type(skin_type)
        return {"Lipstick":lipstick_list,"Foundation":foundation_list,"Blush":blush_list}
        
