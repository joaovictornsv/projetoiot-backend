from azure.cosmos import CosmosClient

import os

URL = os.environ["ACCOUNT_URI"]
KEY = os.environ["ACCOUNT_KEY"]
DATABASE = os.environ["DATABASE_NAME"]
USERS_CONTAINER = os.environ["USERS_CONTAINER"]
LOGS_CONTAINER = os.environ["LOGS_CONTAINER"]

client = CosmosClient(URL, KEY)
database = client.get_database_client(database=DATABASE)


def get_users_container():
    container = database.get_container_client(USERS_CONTAINER)
    return container


def get_logs_container():
    container = database.get_container_client(LOGS_CONTAINER)
    return container
