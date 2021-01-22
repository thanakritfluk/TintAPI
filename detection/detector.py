import cv2
import dlib


# Detect face position return array face array
def face_detect(file_path, file_type):
    img_path = "." + file_path + file_type
    # มันไม่อ่านตั้งแต่ตรงนี้เลย ถ้ามันโดนเรียกมาจาก api
    img = cv2.imread(img_path)

    print("Img path =", img_path)
    print("Img =", img)
    
    image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    grayImg = cv2.equalizeHist(image)
    # Load detector from dlib
    detector = dlib.get_frontal_face_detector()
    # Use detector detect face position
    rectangle_position = detector(img)
    cv2.imwrite("../image/input/source.jpg", img)
    for a in rectangle_position:
        cv2.rectangle(img, (a.left(), a.top()),
                      (a.right(), a.bottom()), (204, 0, 204))
    cv2.imwrite("../image/input/draw_rectangle.jpg", img)
    return rectangle_position, img


# if __name__ == "__main__":
#     img = cv2.imread("../img.jpg")
#     print(face_detect(img))
