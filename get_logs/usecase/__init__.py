from lib.database import get_logs_container


def get_logs_use_case():
    logs_container = get_logs_container()
    logs = logs_container.read_all_items(
        max_item_count=10,
        partition_key="id"
    )
    return list(logs)
