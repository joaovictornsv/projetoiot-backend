import azure.functions as func
from lib.database import get_logs_container
from lib.json import to_json


def get_logs_use_case():
    logs_container = get_logs_container()

    logs = logs_container.read_all_items(
        max_item_count=10,
        partition_key="id"
    )

    return list(logs)


def main(req: func.HttpRequest) -> func.HttpResponse:
    logs = get_logs_use_case()

    response = to_json(logs)

    return func.HttpResponse(response, status_code=200)
