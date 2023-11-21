from uuid import UUID
from app.models.setup_model import Setup
from app.schemas.setup_schema import SetupSchema, SetupCameraSchema
from typing import List
import json
from fastapi import HTTPException, status
import ast
from fastapi import UploadFile, File 

 # File path to store setups
file_path = "Store_Setup.json"

# Function to load setups from file
def load_setups_from_file() -> dict:
    try:
        with open(file_path, "r") as file:
            file_content = file.read()
            if file_content:
                setups = ast.literal_eval(file_content)
                if isinstance(setups, dict):
                    return setups
                else:
                    return {}
            else:
                return {}
    except (FileNotFoundError, SyntaxError):
        return {}

# Function to save setups to file
def save_setups_to_file(setups : SetupSchema):
    with open("Store_Setup.json", "w") as file:
        if setups:
            setups_str_keys = {str(key): value for key, value in setups.items()}
            print(setups_str_keys)
            # Serialize the dictionary to JSON
            setups_json = json.dumps(setups_str_keys, default=str, indent=2)
            # Write the JSON data to the file
            file.write(setups_json)
        else:
            # Handle the case when setups dictionary is empty
            file.write("{}")

# In-memory storage for setups
setup_storage = load_setups_from_file()
print("line 40")
print(setup_storage)


class SetupService:
    @staticmethod
    async def get_cameras() -> List[SetupCameraSchema]:
        load_setups_from_file()
        if not setup_storage:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Setup not found",
            )
        setup = setup_storage
        return setup['camera_zones']

    @staticmethod
    async def create_setup(setup_data: SetupSchema) -> Setup:
        load_setups_from_file()
        new_setup = {**setup_data.dict()}
        print(new_setup)
        save_setups_to_file(new_setup)
        return new_setup
        
    @staticmethod
    async def create_camera(camera_zone: SetupCameraSchema) -> Setup:
        load_setups_from_file()
        if not setup_storage:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Setup not found",
            )

        setup = setup_storage

        # Check if the camera already exists in the setup
        if any(existing_camera['zone_name'] == camera_zone.zone_name for existing_camera in setup['camera_zones']):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Camera zone with the same name already exists in the setup",
            )

        new_camera = {**camera_zone.dict()}  # Use SetupCamera, not Setup
        
        setup['camera_zones'].append(new_camera)
        save_setups_to_file(setup_storage)
        return setup
        
    @staticmethod
    async def update_camera(zone_name: str, camera_zone: SetupCameraSchema) -> Setup:
        load_setups_from_file()
        setup = setup_storage

        # Check if the camera exists in the setup
        existing_camera = next((c for c in setup['camera_zones'] if c['zone_name'] == zone_name), None)
        if not existing_camera:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Camera zone not found in the setup",
            )
        existing_camera = camera_zone.dict()
        print(existing_camera)
        print(camera_zone)
        for i, c in enumerate(setup_storage['camera_zones']):
            if c['zone_name'] == zone_name:
                setup_storage['camera_zones'][i] = existing_camera
        
        save_setups_to_file(setup_storage)
        return setup
    
    @staticmethod
    async def delete_camera(zone_name: str) -> Setup:
        load_setups_from_file()
        setup = setup_storage

        # Check if the camera exists in the setup
        existing_camera = next((c for c in setup.camera_zones if c['zone_name'] == zone_name), None)
        if not existing_camera:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Camera zone not found in the setup",
            )

        setup.camera_zones = [c for c in setup.camera_zones if c['zone_name'] != zone_name]
        save_setups_to_file(setup_storage)
        return setup
    
    @staticmethod
    async def update_setup(setup_id: UUID, setup: Setup) -> Setup:
        load_setups_from_file()
        if setup_id not in setup_storage:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Setup not found",
            )
        new_setup = Setup(**setup.dict())
        setup_storage[setup.setup_id] = new_setup
        save_setups_to_file(setup_storage)
        return setup


    @staticmethod
    async def delete_setup(setup_id: UUID) -> None:
        load_setups_from_file()
        if setup_id not in setup_storage:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Setup not found",
            )

        del setup_storage[setup_id]
        save_setups_to_file({})
        
    
    @staticmethod
    async def get_setup() -> Setup:
        load_setups_from_file() 
        if not setup_storage:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Setup not found",
            )
        print(setup_storage)
        return setup_storage
    
    @staticmethod
    async def list_setups() -> List[Setup]:
        load_setups_from_file()
        return list(setup_storage.values())