import azure.functions as func
import uuid
import logging
from lib.database import get_logs_container
from lib.json import to_json
from lib.storage import upload_blob
import re
from datetime import datetime


def create_log_use_case(data):
    logs_container = get_logs_container()

    data["id"] = str(uuid.uuid4())

    image_base64 = data["image"]
    filename = upload_blob(
        data=image_base64,
        filename=data["id"],
        container="access"
    )
    data["image"] = filename
    data["created_at"] = str(datetime.now())

    user = logs_container.create_item(data)

    return user


def main(req: func.HttpRequest) -> func.HttpResponse:
    body = req.get_json()
    result = create_log_use_case(body)
    response = to_json(result)

    return func.HttpResponse(response, status_code=201)
