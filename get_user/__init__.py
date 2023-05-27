import azure.functions as func
from datetime import datetime
import logging
from lib.database import get_users_container
from lib.json import to_json
from lib.service_bus import send_message_to_log_queue


async def main(req: func.HttpRequest) -> func.HttpResponse:
    user_id = req.route_params.get("id")
    users = get_user_use_case(user_id)
    result = check_user_is_allowed(users)

    data_to_send = {
        "allowed": result["allowed"],
        "user": result["user"]
    }

    await send_log_message(data_to_send)

    response = to_json({
        "allowed": result["allowed"]
    })

    return func.HttpResponse(response, status_code=200)


def get_user_use_case(user_id):
    users_container = get_users_container()

    users = users_container.query_items(
        f"SELECT * FROM users u WHERE u.id = @user_id",
        parameters=[dict(name="@user_id", value=user_id)]
    )

    user_list = list(users)
    return user_list


def check_user_is_allowed(user_list):
    user = None
    user_exists = bool(user_list)

    if user_exists:
        user = user_list[0]

    return {
        "allowed": user_exists,
        "user": user
    }


async def send_log_message(data):
    message = build_message_to_send(data)
    message_json = to_json(message)

    await send_message_to_log_queue(message_json)


def build_message_to_send(data):
    allowed = data["allowed"]
    date_now = datetime.now().isoformat()

    message = {
        "allowed": allowed,
        "date": date_now
    }

    if (allowed):
        message["user_name"] = data["user"]["name"]
        message["user_image"] = data["user"]["profile"]

    return message
