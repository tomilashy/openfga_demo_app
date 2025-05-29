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
        "patient_profiles": {},
        "permissions": {}
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

def create_permission(name: str) -> str:
    """
    Create a permission object with a name.
    If a permission with the same name exists, return its id.
    granted_group_ids is initialized as an empty list.
    Returns the permission id.
    """
    # Check if permission with this name already exists
    for perm in data_store.get("permissions", {}).values():
        if perm.get("name") == name:
            return perm["id"]
    permission_id = str(uuid4())
    data_store.setdefault("permissions", {})
    data_store["permissions"][permission_id] = {
        "id": permission_id,
        "name": name,
        "granted_group_ids": []
    }
    save_data()
    return permission_id

def add_group_to_permission(permission_id: str = None, group_id: str = None, permission_name: str = None):
    """
    Add a group to the granted_group_ids list for a permission.
    Either permission_id or permission_name must be provided.
    """
    if not group_id:
        raise ValueError("group_id must be provided")
    # Find permission by name if id not given
    if not permission_id:
        if not permission_name:
            raise ValueError("Either permission_id or permission_name must be provided")
        # Search for permission by name
        permission = next(
            (perm for perm in data_store.get("permissions", {}).values() if perm.get("name") == permission_name),
            None
        )
        if not permission:
            raise ValueError(f"Permission with name '{permission_name}' not found")
        permission_id = permission["id"]
    else:
        permission = data_store.get("permissions", {}).get(permission_id)
        if not permission:
            raise ValueError(f"Permission with id '{permission_id}' not found")

    if group_id not in permission["granted_group_ids"]:
        permission["granted_group_ids"].append(group_id)
        save_data()

def create_patient_profile(patient_id: str, viewer_permission: str, editor_permission: str) -> str:
    # Check if a profile with the same parameters already exists
    for profile in data_store["patient_profiles"].values():
        if (
            profile["owner"] == patient_id
            # and profile["viewer_permission"] == viewer_permission
            # and profile["editor_permission"] == editor_permission
        ):
            return profile["id"]  # Return existing profile ID

    # Create new profile if not found
    profile_id = str(uuid4())
    data_store["patient_profiles"][profile_id] = {
        "id": profile_id,
        "owner": patient_id,
        "viewer_permission": viewer_permission,
        "editor_permission": editor_permission
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

def get_permission(permission_id: str) -> Dict:
    return data_store.get("permissions", {}).get(permission_id)
