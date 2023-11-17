from uuid import UUID
from app.models.setup_model import Setup
from app.schemas.setup_schema import SetupSchema, SetupCameraSchema
from typing import List
import json
from fastapi import HTTPException, status
import ast

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
def save_setups_to_file(setups):
    with open("Store_Setup.json", "w") as file:
        if setups:
            setups_str_keys = {str(key): value for key, value in setups.items()}
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
    async def create_setup(setup_data: SetupSchema) -> Setup:
    # Check for duplicate data based on shop_name
        existing_setup = next(
            (setup for setup in setup_storage.values() if isinstance(setup, Setup) and setup.shop_name == setup_data.shop_name),
            None
        )

        if existing_setup:
            # Handle duplicate data, for example, you can raise an HTTPException
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Setup with the same shop_name already exists",
            )

        new_setup = Setup(**setup_data.dict())
        setup_storage[new_setup.setup_id] = new_setup
        save_setups_to_file(setup_storage)
        return new_setup
        
    @staticmethod
    async def create_camera(setup_id: UUID, camera_zone: SetupCameraSchema) -> Setup:
        if setup_id not in setup_storage:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Setup not found",
            )

        setup = setup_storage[setup_id]

        # Check if the camera already exists in the setup
        if any(existing_camera.zone_name == camera_zone.zone_name for existing_camera in setup.camera_zones):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Camera zone with the same name already exists in the setup",
            )

        new_camera = SetupCameraSchema(**camera_zone.dict())  # Use SetupCamera, not Setup
        setup.camera_zones.append(new_camera)
        save_setups_to_file(setup_storage)
        return setup

        
    @staticmethod
    async def update_camera(setup_id: UUID, zone_name: str, camera_zone: SetupCameraSchema) -> Setup:
        if setup_id not in setup_storage:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Setup not found",
            )

        setup = setup_storage[setup_id]

        # Check if the camera exists in the setup
        existing_camera = next((c for c in setup.camera_zones if c.zone_name == zone_name), None)
        if not existing_camera:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Camera zone not found in the setup",
            )

        existing_camera= camera_zone
        save_setups_to_file(setup_storage)
        return setup
    @staticmethod
    async def delete_camera(setup_id: UUID, zone_name: str) -> Setup:
        if setup_id not in setup_storage:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Setup not found",
            )

        setup = setup_storage[setup_id]

        # Check if the camera exists in the setup
        existing_camera = next((c for c in setup.camera_zones if c.zone_name == zone_name), None)
        if not existing_camera:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Camera zone not found in the setup",
            )

        setup.camera_zones = [c for c in setup.camera_zones if c.zone_name != zone_name]
        save_setups_to_file(setup_storage)
        return setup
    
    @staticmethod
    async def update_setup(setup_id: UUID, setup: Setup) -> Setup:
        if setup_id not in setup_storage:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Setup not found",
            )
        new_setup = Setup(**setup.dict())
        setup_storage[new_setup.setup_id] = new_setup
        save_setups_to_file(setup_storage)
        return setup


    @staticmethod
    async def delete_setup(setup_id: UUID) -> None:
        if setup_id not in setup_storage:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Setup not found",
            )

        del setup_storage[setup_id]
        save_setups_to_file({})
        
    
    @staticmethod
    async def get_setup_by_id(setup_id: UUID) -> Setup:
        if setup_id not in setup_storage:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Setup not found",
            )

        return setup_storage[setup_id]
    
    @staticmethod
    async def list_setups() -> List[Setup]:
        return list(setup_storage.values())
