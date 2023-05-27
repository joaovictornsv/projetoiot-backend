import azure.functions as func
import uuid
import logging
from lib.database import get_users_container
from lib.json import to_json
from lib.storage import upload_blob
import re


def create_user_use_case(data):
    users_container = get_users_container()

    data["id"] = str(uuid.uuid4())

    profile_image_base64 = data["profile"]
    filename = upload_blob(
        data=profile_image_base64,
        filename=data["id"],
        container="users"
    )
    data["profile"] = filename

    user = users_container.create_item(data)

    return user


def main(req: func.HttpRequest) -> func.HttpResponse:
    body = req.get_json()
    result = create_user_use_case(body)
    response = to_json(result)

    return func.HttpResponse(response, status_code=201)
