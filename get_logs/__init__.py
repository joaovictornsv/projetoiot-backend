import logging
import json
import azure.functions as func
from .usecase import get_logs_use_case


def main(req: func.HttpRequest) -> func.HttpResponse:
    logs = get_logs_use_case()

    response = json.dumps(logs)

    return func.HttpResponse(response, status_code=200)
