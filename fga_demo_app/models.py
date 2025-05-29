import json
import os
from typing import Dict
from uuid import uuid4

DATA_FILE = "data_store.json"

# Initialize data containers
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        data_store = json.load(f)
else:
    data_store = {
        "users": {},
        "groups": {},
        "patient_profiles": {}
    }

def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump(data_store, f, indent=4)

def create_user(name: str) -> str:
    # Check if user already exists by name, to avoid duplicates
    for user in data_store["users"].values():
        if user["name"] == name:
            return user["id"]

    user_id = str(uuid4())
    data_store["users"][user_id] = {"id": user_id, "name": name}
    save_data()
    return user_id

def create_group(name: str) -> str:
    # Check if group already exists by name
    for group in data_store["groups"].values():
        if group["name"] == name:
            return group["id"]

    group_id = str(uuid4())
    data_store["groups"][group_id] = {"id": group_id, "name": name, "members": []}
    save_data()
    return group_id

def add_user_to_group(user_id: str, group_id: str):
    group = data_store["groups"].get(group_id)
    if group and user_id not in group["members"]:
        group["members"].append(user_id)
        save_data()

def create_patient_profile(patient_id: str, viewer_group: str, editor_group: str) -> str:
    # Check if a profile with the same parameters already exists
    for profile in data_store["patient_profiles"].values():
        if (
            profile["owner"] == patient_id
            # profile["viewer_group"] == viewer_group and
            # profile["editor_group"] == editor_group
        ):
            return profile["id"]  # Return existing profile ID

    # Create new profile if not found
    profile_id = str(uuid4())
    data_store["patient_profiles"][profile_id] = {
        "id": profile_id,
        "owner": patient_id,
        "viewer_group": viewer_group,
        "editor_group": editor_group
    }
    save_data()
    return profile_id

# Optional getters

def get_user(user_id: str) -> Dict:
    return data_store["users"].get(user_id)

def get_group(group_id: str) -> Dict:
    return data_store["groups"].get(group_id)

def get_patient_profile(profile_id: str) -> Dict:
    return data_store["patient_profiles"].get(profile_id)
