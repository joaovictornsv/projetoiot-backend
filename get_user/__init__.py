import json
import azure.functions as func
from lib.database import get_users_container
import logging


def get_user_use_case(user_id):
    users_container = get_users_container()

    users = users_container.query_items(
        f"SELECT * FROM users u WHERE u.id = {user_id}"
    )

    user_length = len(list(users))
    user_exists = bool(user_length)
    result = {
        "allowed": user_exists
    }
    return result


def main(req: func.HttpRequest) -> func.HttpResponse:
    user_id = req.route_params.get("id")
    access_result = get_user_use_case(user_id)
    response = json.dumps(access_result)

    return func.HttpResponse(response, status_code=200)
