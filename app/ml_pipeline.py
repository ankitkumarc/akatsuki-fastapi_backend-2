import ultralytics
from ultralytics import YOLO
import supervision as sv

from ml_object_handler.inference import Inference

inference_obj = Inference()
byte_tracker = sv.ByteTrack()
annotator = sv.BoxAnnotator()
import numpy as np
heat_map_annotator = sv.HeatMapAnnotator()


start=sv.Point(0,280)
end = sv.Point(960,280)

line_zone = sv.LineZone(start,end)
line_annot = sv.LineZoneAnnotator()
def process_frame_heatmap(frame: np.ndarray, index: int) -> np.ndarray:
    results = inference_obj.predict(frame,obj='person')[0]
    detections = sv.Detections.from_ultralytics(results)
    detections=detections[detections.class_id==0]
    #import pdb;pdb.set_trace()
    
    
    detections = byte_tracker.update_with_detections(detections)
    count = line_zone.trigger(detections=detections)
    print('count',sum(count[0]),sum(count[1]))
    labels = [
        f"#{tracker_id} {inference_obj.person_detector_model.names[class_id]} {confidence:0.2f}"
       for _, _, confidence, class_id, tracker_id
      in detections
   ]
    #blurred_frame = blur_faces(frame)
    #import pdb;pdb.set_trace()
    annot_frame = line_annot.annotate(frame=frame.copy(),line_counter=line_zone)
    annotated_frame  = annotator.annotate(scene=annot_frame, detections=detections, labels=labels)
    return heat_map_annotator.annotate(scene=annotated_frame,detections=detections)


sv.process_video(source_path='../inp_vids/cctv_entrance.mp4', target_path=f"people_count_cctv_entrance.mp4", callback=process_frame_heatmap)