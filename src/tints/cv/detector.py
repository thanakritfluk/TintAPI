import cv2
import dlib
import numpy as np
from os.path import join as pjoin
from src.tints.settings import COLOR_PREDICTION_INPUT,COLOR_PREDICTION_OUTPUT,SHAPE_68_PATH,SAVE_FILE_TYPE


PREDICTOR_PATH = SHAPE_68_PATH
class DetectLandmarks(object):

    IMAGE_DATA = 'IMAGE_DATA'
    FILE_READ = 'FILE_READ'
    NETWORK_BYTE_STREAM = 'NETWORK_BYTE_STREAM'
    COLOR_PREDICTION_FILE_READ = "COLOR_PREDICTION_FILE_READ"

    def __init__(self):
        self.predictor = dlib.shape_predictor(PREDICTOR_PATH)
        self.detector = dlib.get_frontal_face_detector()



    def get_landmarks(self, image):
        """ Extract the landmarks from a given image. 
        Returns `None` if no landmarks found.
        """
        try:
            rects = self.detector(image, 1)
            size = len(rects)
            image = cv2.cvtColor(np.copy(image), cv2.COLOR_BGR2GRAY)
            grayImg = cv2.equalizeHist(image)
            if size == 0:
                return None, None
            return np.matrix([[p.x, p.y] for p in self.predictor(grayImg, rects[0]).parts()])
        except Exception:
            return None



    def get_face_data(self, image_file, flag = None):
        """
        Returns all facial landmarks in a given image.
        """
        image = 0
        if flag == self.FILE_READ:
            image = cv2.imread(image_file)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        elif flag == self.NETWORK_BYTE_STREAM:
            image = cv2.imdecode(
                np.fromstring(image_file.read(), np.uint8), cv2.IMREAD_UNCHANGED
            )
        elif flag == self.IMAGE_DATA or flag is None:
            image = image_file
            landmarks = self.get_landmarks(image)
        elif flag == self.COLOR_PREDICTION_FILE_READ:
            image = cv2.imread(image_file)
            landmarks = self.get_landmarks(image)
        if landmarks[0] is None or landmarks[1] is None:
            return None
        return landmarks

    def save_localize_lanmark_image(self, image,output_path,output_name,flag=None):
        if flag == self.COLOR_PREDICTION_FILE_READ:
            image_data = cv2.imread(image)
            image_copy = np.copy(image_data)
        else:
            image_copy = np.copy(image)
        lanmarks = self.get_face_data(image_file=image,flag=flag)
        for (i,point) in enumerate(lanmarks):
            x = point[0,0]
            y = point[0,1]
            cv2.circle(np.float32(image_copy),(x,y),1,(0,255,255),-1)
            cv2.putText(image_copy, "{}".format(i+1), (x,y-2),cv2.FONT_HERSHEY_SIMPLEX,0.6,(0,255,0),2)
        cv2.imwrite(pjoin(output_path,"".join((output_name,SAVE_FILE_TYPE))) , image_copy)    

    def convert_request_files_to_image(self,request_file):
        return cv2.imdecode(np.fromstring(request_file.read(), np.uint8), cv2.IMREAD_COLOR)


    def create_box(self, image, output_path, output_name, np_points, flag=None):
        if flag == self.COLOR_PREDICTION_FILE_READ:
            image = cv2.imread(image)
        mask = np.zeros_like(image)
        # Our feature
        mask = cv2.fillPoly(mask, [np_points], (255,255,255))
        # cv2.imwrite(pjoin(output_path,"Mask.jpg"), mask)   
        image = cv2.bitwise_and(image,mask)
        # cv2.imwrite(pjoin( APP_OUTPUT,"OnlyLipIMG.jpg"), img)  
        bbox = cv2.boundingRect(np_points)
        x,y,w,h = bbox
        image_crop = image[y: y + h, x: x + w]
        # print("Crop=",image_crop)
        cv2.imwrite(pjoin( output_path,"".join((output_name,SAVE_FILE_TYPE))), image_crop)
        # imgCrop = cv2.resize(imgCrop, (0,0), None, scale, scale)
        # return imgCrop

    def get_cheek_np(self, image, flag=None):
        """
        Return points for cheek as np array in given image
        """
        lanmarks = self.get_face_data(image_file=image, flag=flag)
        np_list = np.concatenate((lanmarks[2],lanmarks[3],lanmarks[4], lanmarks[5],lanmarks[49],lanmarks[29],lanmarks[40]))
        return np_list


    def get_lip_np(self, image, flag=None):
        """
        Returns points for lips as np array in given image.
        """
        lanmarks = self.get_face_data(image_file=image, flag=flag)
        return lanmarks[48:]

    def get_lips(self, image_file, flag=None):
        """
        Returns points for lips in given image.
        """
        landmarks = self.get_face_data(image_file, flag)
        if landmarks is None:
            return None
        lips = ""
        for point in landmarks[48:]:
            lips += str(point).replace('[', '').replace(']', '') + '\n'
        return lips


