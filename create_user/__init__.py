import json
import azure.functions as func
from lib.database import get_users_container
import logging
import uuid


def create_user_use_case(data):
    users_container = get_users_container()

    data["id"] = str(uuid.uuid4())
    user = users_container.create_item(data)

    return user


def main(req: func.HttpRequest) -> func.HttpResponse:
    body = req.get_json()
    result = create_user_use_case(body)
    response = json.dumps(result)

    return func.HttpResponse(response, status_code=200)
