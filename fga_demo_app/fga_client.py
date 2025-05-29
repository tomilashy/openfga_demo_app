from openfga_sdk import OpenFgaClient, ClientConfiguration, TupleKey
from openfga_sdk.client.models import ClientTuple, ClientWriteRequest, ClientCheckRequest
from openfga_sdk.exceptions import ValidationException
import httpx
from dotenv import load_dotenv
import os

load_dotenv()

OPENFGA_API_SCHEME = os.environ["OPENFGA_API_SCHEME"]
OPENFGA_API_HOST = os.environ["OPENFGA_API_HOST"]
OPENFGA_STORE_ID = os.environ["OPENFGA_STORE_ID"]
AUTHORIZATION_MODEL_ID = os.environ["AUTHORIZATION_MODEL_ID"]

# Configure your FGA instance
fga_client = OpenFgaClient(
    ClientConfiguration(
        api_scheme=OPENFGA_API_SCHEME,
        api_host=OPENFGA_API_HOST,
        store_id=OPENFGA_STORE_ID
    )
)

options = {
    "authorization_model_id": AUTHORIZATION_MODEL_ID
}
# async def assign_tuple(user: str, relation: str, object_: str):
#     await fga_client.write([TupleKey(user=user, relation=relation, object=object_)])

# async def check_permission(user: str, relation: str, object_: str) -> bool:
#     response = await fga_client.check(user=user, relation=relation, object=object_)
#     return response.allowed


async def assign_tuple_raw(user: str, relation: str, object_: str):
    # Only prefix 'user:' if not already a reference (i.e., no colon in user)
    # if ':' in user:
    #     user_field = user
    # else:
    #     user_field = f"user:{user}"
    url = f"{OPENFGA_API_SCHEME}://{OPENFGA_API_HOST}/stores/{OPENFGA_STORE_ID}/write"
    payload = {
            "writes": {
                "tuple_keys": [
                    {
                        "user": user,
                        "relation": relation,
                        "object": object_,
                    }
                ]
            },
            "authorization_model_id": AUTHORIZATION_MODEL_ID
        }

    headers = {
        "Content-Type": "application/json"
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        print("Tuple successfully written.")
    else:
        print(f"Error writing tuple: {response.status_code}")
        print(response.text)
        # response.raise_for_status()

async def assign_tuple(user: str, relation: str, object_: str):
    """
    Assigns a relationship tuple in OpenFGA.
    Equivalent to saying: user <relation> object
    Example: user:alice is the owner of patient_profile:123
    """
    tuple_ = ClientTuple(
        user=f"user:{user}",
        relation=relation,
        object=object_
    )
    write_request = ClientWriteRequest(writes=[tuple_])
    try:
        await fga_client.write(write_request, options)
    except Exception as e:
        print("Full error (fallback):", str(e))
        raise

async def check_permission(user: str, relation: str, object_: str) -> bool:
    """
    Checks if a user has a given permission on an object.
    """
    check_request = ClientCheckRequest(
        user=f"user:{user}",
        relation=relation,
        object=object_
    )

    response = await fga_client.check(check_request, options)
    return response.allowed

async def check_permission_raw(user: str, relation: str, object_: str):
    # Only prefix 'user:' if not already a reference (i.e., no colon in user)
    if ':' in user:
        user_field = user
    else:
        user_field = f"user:{user}"

    url = f"{OPENFGA_API_SCHEME}://{OPENFGA_API_HOST}/stores/{OPENFGA_STORE_ID}/check"
    payload = {
        "tuple_key": {
            "user": user_field,
            "relation": relation,
            "object": object_
        },
        # "contextual_tuples": { "tuple_keys": [...] },  # Optional, not used here
        "authorization_model_id": AUTHORIZATION_MODEL_ID
    }
    headers = {
        "Content-Type": "application/json"
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data.get("allowed", False)
    else:
        print(f"Error checking permission: {response.status_code}")
        print(response.text)
        return False