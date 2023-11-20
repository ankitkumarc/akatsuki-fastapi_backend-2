from fastapi import APIRouter
from app.services.setup_service import SetupService
from app.schemas.setup_schema import SetupSchema, SetupCameraSchema
from uuid import UUID
from fastapi import UploadFile, File
from fastapi import Depends

setup_router = APIRouter()

@setup_router.post('/', summary="Create Setup")
async def create_setup(data: SetupSchema):
    new_setup = await SetupService.create_setup(data)
    return {"message": "Setup created successfully", "setup": new_setup}

@setup_router.put("/update_setup/{setup_id}")
async def update_setup(setup_id: UUID, data: SetupSchema):
    updated_setup = await SetupService.update_setup(setup_id, data)
    return updated_setup

@setup_router.delete('/{setup_id}', summary="Delete Setup")
async def delete_setup():
    return await SetupService.delete_setup()

@setup_router.post('/camera', summary="Add Camera Zone")
async def add_camera_zone(camera_zone: SetupCameraSchema):
    return await SetupService.create_camera(camera_zone)

@setup_router.get('/cameras', summary="Get Setups")
async def get_cameras():
    return await SetupService.get_cameras()
    

@setup_router.put('/camera/{zone_name}', summary="Update Camera Zone")
async def update_camera_zone(zone_name: str, camera_zone: SetupCameraSchema):
    return await SetupService.update_camera(zone_name, camera_zone)

# @setup_router.delete('/{setup_id}/camera/{zone_name}', summary="Delete Camera Zone")
# async def delete_camera_zone(setup_id: UUID, zone_name: str):
#     return await SetupService.delete_camera(setup_id, zone_name)

@setup_router.get('/', summary="Get Setups")
async def get_setup():
    return await SetupService.get_setup()