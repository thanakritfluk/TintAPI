import cv2
import dlib
import numpy as np
from os.path import join as pjoin
from src.tints.settings import APP_INPUT,APP_OUTPUT,SHAPE_68_PATH
from src.tints.cv.lipstick_detection import predict_lipstick_color


def createBox(img, points, scale=1):
    mask = np.zeros_like(img)
    # Our feature
    mask = cv2.fillPoly(mask, [points], (255,255,255))
    cv2.imwrite(pjoin( APP_OUTPUT,"Mask.jpg"), mask)   
    img = cv2.bitwise_and(img,mask)
    # cv2.imwrite(pjoin( APP_OUTPUT,"OnlyLipIMG.jpg"), img)  
    bbox = cv2.boundingRect(points)
    x,y,w,h = bbox
    imgCrop = img[y:y+h, x:x+w]
    # imgCrop = cv2.resize(imgCrop, (0,0), None, scale, scale)
    return imgCrop


# Detect face position return array face array
def face_detect(img, userID):
    #Setting name of picture
    SOURCE_NAME = "".join(("Source_",userID,".jpg"))
    LANMARK_NAME = "".join(("LanmarkPoint_",userID,".jpg"))
    LIPAREA_NAME = "".join(("LipArea_",userID,".jpg"))
    CHEEKAREA_NAME = "".join(("CheekArea_",userID,".jpg"))
    img = cv2.imdecode(np.fromstring(img.read(), np.uint8), cv2.IMREAD_COLOR)
    image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    grayImg = cv2.equalizeHist(image)
    # Load detector from dlib
    detector = dlib.get_frontal_face_detector()
    # Use detector detect rectangle face position
    rectangle_position = detector(img, 1)
    cv2.imwrite(pjoin(APP_INPUT, SOURCE_NAME),img)
    for a in rectangle_position:
        cv2.rectangle(img, (a.left(), a.top()),
                      (a.right(), a.bottom()), (204, 0, 204))
    # Load model facial lanmark                  
    predictor = dlib.shape_predictor(SHAPE_68_PATH)
    lip_point = []
    cheek_point =[]
    lanmark_img = np.copy(img)
    for index, face in enumerate(rectangle_position,0):
        shape = predictor(grayImg, face)
        for i, pt in enumerate(shape.parts()):
            pt_pos = (pt.x, pt.y)
            cv2.circle(lanmark_img, pt_pos, 2, (255, 255, 255), 2)
            # Collect lip area
            if i >= 48 and i <= 67:
                lip_point.append([pt.x,pt.y])
            # Collect left cheek area
            if i>=2 and i<=5 or i ==29  or i== 40 or i ==49:
                cheek_point.append([pt.x,pt.y])
    # Swap index to drawing cheek area
    cheek_point[4], cheek_point[6] = cheek_point[6], cheek_point[4]
    cheek_point[5], cheek_point[6] = cheek_point[6], cheek_point[5]
    cv2.imwrite(pjoin( APP_INPUT,LANMARK_NAME), lanmark_img) 
    # Lip area crop   
    lip_point = np.array(lip_point)
    crop_lip = createBox(img, lip_point[0:len(lip_point)+1])
    cv2.imwrite(pjoin( APP_OUTPUT,LIPAREA_NAME), crop_lip)
    # Cheek area crop
    cheek_point = np.array(cheek_point)
    print("Cheek point=",cheek_point)
    crop_cheek = createBox(img, cheek_point[0:len(cheek_point)])
    cv2.imwrite(pjoin( APP_OUTPUT,CHEEKAREA_NAME), crop_cheek)

def color_detection(ref_img, userID):
    face_detect(ref_img,userID)
    return predict_lipstick_color(userID)



# if __name__ == "__main__":
#     img = cv2.imread("../img.jpg")
#     print(face_detect(img))
