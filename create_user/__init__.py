import azure.functions as func
import uuid
import logging
from lib.database import get_users_container
from lib.json import to_json


def create_user_use_case(data):
    users_container = get_users_container()

    data["id"] = str(uuid.uuid4())
    user = users_container.create_item(data)

    return user


def main(req: func.HttpRequest) -> func.HttpResponse:
    body = req.get_json()
    result = create_user_use_case(body)
    response = to_json(result)

    return func.HttpResponse(response, status_code=200)
