# settings.py
import os
# __file__ refers to the file settings.py
APP_ROOT = os.path.dirname(os.path.abspath(
    __file__))   # refers to application_top
COLOR_PREDICTION_INPUT = os.path.join(
    APP_ROOT, './image/color_prediction_input')
COLOR_PREDICTION_OUTPUT = os.path.join(
    APP_ROOT, './image/color_prediction_output')
SIMULATOR_INPUT = os.path.join(APP_ROOT, './image/simulator_input')
SIMULATOR_OUTPUT = os.path.join(APP_ROOT, './image/simulator_output')
SHAPE_68_PATH = os.path.join(
    APP_ROOT, './cv/train_model/shape_predictor_68_face_landmarks.dat')

# Lipstick settings
METHOD_NUM = 2
BLACK_THRESHOLD = 20
COLOR_COMPARE_VAL = 15
RETURN_SIZE = 100

# Kmean settings
NUMBER_K = 5
RETURN_INDEX = 2
