import azure.functions as func
from lib.database import get_logs_container
from lib.json import to_json
from lib.storage import generate_sas_url


def get_logs_use_case():
    logs_container = get_logs_container()

    logs = logs_container.query_items(
        "SELECT * FROM access_logs a ORDER BY a._ts DESC OFFSET 0 LIMIT 10",
        enable_cross_partition_query=True,
    )

    list_logs = list(logs)

    for log in list_logs:
        log_dict = dict(log)
        user_image = log_dict.get("user_image", '')
        if not user_image:
            continue

        url = generate_sas_url(user_image, "users")
        log["user_image"] = url

    return list_logs


def main(req: func.HttpRequest) -> func.HttpResponse:
    logs = get_logs_use_case()

    response = to_json(logs)

    return func.HttpResponse(response, status_code=200)
