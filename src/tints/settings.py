#settings.py
import os
# __file__ refers to the file settings.py 
APP_ROOT = os.path.dirname(os.path.abspath(__file__))   # refers to application_top
APP_INPUT = os.path.join(APP_ROOT, './image/input')
APP_OUTPUT = os.path.join(APP_ROOT, './image/output')
SHAPE_68_PATH = os.path.join(APP_ROOT, './cv/shape_predictor_68_face_landmarks.dat')
COLOR_COMPARE_VAL = 15

# Kmean settings
NUMBER_K = 5
RETURN_INDEX = 2