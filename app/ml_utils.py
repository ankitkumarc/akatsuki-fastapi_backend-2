import argparse
from typing import Dict, List, Set, Tuple
from app.ml_object_handler.person import People
import cv2
import numpy as np
from tqdm import tqdm
from ultralytics import YOLO
from shapely.geometry import Polygon, Point
import supervision as sv

COLORS = sv.ColorPalette.default()

ZONE_IN_POLYGONS = [
    np.array([[592, 282], [600, 282], [600, 82], [592, 82]]),
    np.array([[300, 460], [600, 460], [600, 700], [300, 700]]),
    
]
zone_icecream = [[970,5],[1250,5],[1250,483],[970,483]]
zone_chocolate = [[715,9],[853,9],[853,260],[715,260]]
zone_juice = [[604,7],[708,7],[708,193],[604,193]]
all_zones = [zone_icecream,zone_chocolate,zone_juice]
all_zone_names= ['zone_juice','zone_chocolate','zone_icecream']

class DetectionsManager:
    def __init__(self) -> None:
        self.tracker_id_to_zone_id: Dict[int, int] = {}
        self.counts: Dict[int, Dict[int, Set[int]]] = {}

    def update(
        self,
        detections_all: sv.Detections,
        detections_in_zones: List[sv.Detections],
        detections_out_zones: List[sv.Detections],
    ) -> sv.Detections:
        for zone_in_id, detections_in_zone in enumerate(detections_in_zones):
            for tracker_id in detections_in_zone.tracker_id:
                self.tracker_id_to_zone_id.setdefault(tracker_id, zone_in_id)        

        detections_all.class_id = np.vectorize(
            lambda x: self.tracker_id_to_zone_id.get(x, -1)
        )(detections_all.tracker_id)
        return detections_all[detections_all.class_id != -1]


def initiate_polygon_zones(
    polygons: List[np.ndarray],
    frame_resolution_wh: Tuple[int, int],
    triggering_position: sv.Position = sv.Position.CENTER,
) -> List[sv.PolygonZone]:
    return [
        sv.PolygonZone(
            polygon=polygon,
            frame_resolution_wh=frame_resolution_wh,
            triggering_position=triggering_position,
        )
        for polygon in polygons
    ]



def count_points_in_zones(polygons, points):
    zone_points_count = {i: 0 for i in range(len(polygons))}

    # Create Polygon objects for each zone
    zone_polygons = [Polygon(zone) for zone in polygons]

    # Check each point against each zone

    all_zone_pts = 0
    for point in points:
        point = Point(point)
        for i, zone_polygon in enumerate(zone_polygons):
            if zone_polygon.contains(point):
                zone_points_count[i] += 1
        all_zone_pts+=zone_points_count[i]
    #import pdb;pdb.set_trace()
    for i in range(len(polygons)):
        zone_pct = (zone_points_count[i]/sum(zone_points_count.values()))*100
        print('Occupancy of '+ all_zone_names[i] +':' +str(zone_pct) +'%')
    return zone_points_count
class VideoProcessor:
    def __init__(
        self,
        inferenece_obj: object,
        source_video_path: str,
        confidence_threshold: float = 0.3,
        iou_threshold: float = 0.7,
        camera_type: str = 'product',
        zones : List = all_zones
    ) -> None:
        self.conf_threshold = confidence_threshold
        self.iou_threshold = iou_threshold
        self.source_video_path = source_video_path
        #import pdb;pdb.set_trace()
        self.target_video_path = self.source_video_path.split('/')[-1].split('.')[0] + "_output.mp4"
        self.zones = zones
        self.model = inferenece_obj
        self.tracker = sv.ByteTrack()
        self.camera_type = camera_type
        self.video_info = sv.VideoInfo.from_video_path(source_video_path)
        self.zones_in = initiate_polygon_zones(
            ZONE_IN_POLYGONS, self.video_info.resolution_wh, sv.Position.CENTER
        )
        
        self.box_annotator = sv.BoxAnnotator(color=COLORS)
        self.trace_annotator = sv.TraceAnnotator(
            color=COLORS, position=sv.Position.TOP_LEFT, trace_length=100, thickness=1
        )
        self.heat_map_annotator = sv.HeatMapAnnotator()
        self.detections_manager = DetectionsManager()
        self.person_obj_dict = {}

    def process_video(self):
        frame_generator = sv.get_video_frames_generator(
            source_path=self.source_video_path
        )

        if self.target_video_path:
            with sv.VideoSink(self.target_video_path, self.video_info) as sink:
                for frame in tqdm(frame_generator, total=self.video_info.total_frames):
                    annotated_frame = self.process_frame(frame)
                    sink.write_frame(annotated_frame)
        else:
            for frame in tqdm(frame_generator, total=self.video_info.total_frames):
                annotated_frame = self.process_frame(frame)
                cv2.imshow("Processed Video", annotated_frame)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
            cv2.destroyAllWindows()
        
        zone_points_list = []

        for key in self.person_obj_dict.keys():
            person_zone_points = self.person_obj_dict[key].history
            zone_points_list.extend(person_zone_points)
        #print(zone_points_list)
        if self.zones:
            zone_points_count = count_points_in_zones(self.zones, zone_points_list)
        print(zone_points_count)
        

    def annotate_frame(
        self, frame: np.ndarray, detections: sv.Detections
    ) -> np.ndarray:
        annotated_frame = frame.copy()
        
        labels = [f"#{tracker_id}" for tracker_id in detections.tracker_id]
        if self.camera_type=='entrance':
            annotated_frame = self.trace_annotator.annotate(annotated_frame, detections)
        else:
            annotated_frame = self.heat_map_annotator.annotate(annotated_frame, detections)
        annotated_frame = self.box_annotator.annotate(
            annotated_frame, detections, labels
        )

        

        return annotated_frame

    def process_frame(self, frame: np.ndarray) -> np.ndarray:
        results = self.model.person_detector_model(
            frame, verbose=False, conf=self.conf_threshold, iou=self.iou_threshold
        )[0]
        detections = sv.Detections.from_ultralytics(results)
        detections = detections[detections.class_id == 0]
        detections.class_id = np.zeros(len(detections))
        detections = self.tracker.update_with_detections(detections)
        for (tracker_id,box,tracker_obj)  in zip(detections.tracker_id,detections.xyxy,self.tracker.tracked_tracks) :
            if tracker_id in self.person_obj_dict.keys():
                person_obj = self.person_obj_dict[tracker_id]
                person_obj.end_time = tracker_obj.end_frame

                person_obj.history.append((box[0]+box[2]*0.5,box[1]+box[3]*0.5))
            else:    
                self.person_obj_dict.setdefault(tracker_id, People(box,tracker_id,tracker_obj))

        #print('Tracked tracks:',self.tracker.tracked_tracks)
        #print('Removed tracks:',self.tracker.removed_tracks)
        #import pdb;pdb.set_trace()


        
        return self.annotate_frame(frame, detections)