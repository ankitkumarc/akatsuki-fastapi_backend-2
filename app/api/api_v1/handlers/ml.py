from fastapi import APIRouter, Depends,HTTPException
from app.schemas.customer_schema import CustomerOut, CustomerCreate, CustomerUpdate
from app.api.deps.retailer_deps import get_current_user
from app.models.retailer_model import User
from app.services.customer_service import CustomerService
from app.models.customer_model import Customer
from uuid import UUID
from typing import List
import ultralytics

from app.ml_object_handler.inference import Inference
from app.ml_utils import VideoProcessor,DetectionsManager
infer_obj = Inference()


ml_router = APIRouter()


@ml_router.post('/start_processing', summary="Start ML video processing")
async def start_processing(video_list: List[str]):
    video_list=['/media/pritesh/F_drive/retailsense-backend/inp_vids/cctv_entrance.mp4']
    for v_path in video_list:
        video_processor = VideoProcessor(inferenece_obj=infer_obj,source_video_path=v_path)
        op = video_processor.process_video()
    
    
    return {'message':"Sucess"}