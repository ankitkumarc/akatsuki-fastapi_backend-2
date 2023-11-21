import ultralytics
from ultralytics import YOLO
import supervision as sv

from ml_object_handler.inference import Inference
from ml_utils import VideoProcessor,DetectionsManager
infer_obj = Inference()

video_processor = VideoProcessor(inferenece_obj=infer_obj,source_video_path='../inp_vids/nana.mp4')
video_processor.process_video()
import pdb;pdb.set_trace()