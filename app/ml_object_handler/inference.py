import torch
import cv2 
import numpy as np 
from ultralytics import YOLO
from ultralytics import YOLO
import supervision as sv
from keras.models import load_model


# Load the YOLOv5 model
# model_path = ' yolov5s.pt'
#odel_path = 'crowdhuman_yolov5m.pt'


class Inference():
    
    def __init__(self):
        
        self.age_gender_model = load_model('./app/ml_object_handler/model_weights/age_gender/model.h5')
        self.person_detector_model=YOLO('./app/ml_object_handler/model_weights/person_detection/yolov8l.pt')        
        # self.__has_uniform = None

    def predict(self,frame,obj='person'):
        if obj=='person':
            result = self.person_detector_model(frame)
        else :
            result = self.age_gender_model(frame)

        return result

