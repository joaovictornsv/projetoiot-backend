import logging
import json
import azure.functions as func
from lib.database import get_logs_container
import uuid


def create_log_use_case(log_data):
    logs_container = get_logs_container()

    log_data["id"] = str(uuid.uuid4())
    logs_container.create_item(log_data)


def main(msg: func.ServiceBusMessage):
    message_body = json.loads(msg.get_body().decode("utf-8"))
    create_log_use_case(message_body)
