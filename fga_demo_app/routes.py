from fastapi import APIRouter
from fga_demo_app import models
from fga_demo_app.fga_client import assign_tuple, check_permission, assign_tuple_raw, check_permission_raw
# from fga_demo_app.data import mock_users, mock_groups

router = APIRouter()

@router.get("/setup")
async def setup_demo():
    # Create users
    alice = models.create_user("Alice (Patient)")
    bob = models.create_user("Bob (Doctor)")
    chris = models.create_user("Chris (Nurse)")

    # Create groups
    viewer_group = models.create_group("Viewer Group")
    editor_group = models.create_group("Editor Group")

    # Add users to groups
    models.add_user_to_group(bob, viewer_group)
    models.add_user_to_group(chris, editor_group)

    # Create profile
    profile_id = models.create_patient_profile(
        patient_id=alice,
        viewer_group=viewer_group,
        editor_group=editor_group
    )

    # Push relations to OpenFGA
    await assign_tuple_raw(user=f"user:{alice}", relation="owner", object_=f"patient_profile:{profile_id}")
    await assign_tuple_raw(user=f"group:{viewer_group}#member", relation="viewer_group", object_=f"patient_profile:{profile_id}")
    await assign_tuple_raw(user=f"group:{editor_group}#member", relation="editor_group", object_=f"patient_profile:{profile_id}")
    # await assign_tuple_raw(user=f"group:{viewer_group}", relation="viewer_group", object_=f"patient_profile:{profile_id}")
    # await assign_tuple_raw(user=f"group:{editor_group}", relation="editor_group", object_=f"patient_profile:{profile_id}")
    await assign_tuple_raw(user=f"user:{bob}", relation="member", object_=f"group:{viewer_group}")
    await assign_tuple_raw(user=f"user:{chris}", relation="member", object_=f"group:{editor_group}")

    return {
        "patient_profile_id": profile_id,
        "users": {"alice": alice, "bob": bob, "chris": chris}
    }

@router.get("/check/{user_id}/{action}/{profile_id}")
async def check(user_id: str, action: str, profile_id: str):
    object_ = f"patient_profile:{profile_id}"
    is_allowed = await check_permission_raw(user_id, action, object_)
    profile = models.get_patient_profile(profile_id).get("owner")
    # return {"user": user_id, "action": action, "object": profile_id, "allowed": is_allowed}
    return { "user": models.get_user(user_id).get("name"), "action": action, "object": models.get_user(profile).get("name"), "allowed": is_allowed}


@router.get("/hello")
async def hello():
    return {"message": "Hello, world!"}