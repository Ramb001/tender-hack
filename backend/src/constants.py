import os

from pocketbase_api import Pocketbase

POCKETBASE_URL = "http://127.0.0.1:8090"
PB = Pocketbase(POCKETBASE_URL)

RAGFLOW_API_KEY = os.getenv("RAGFLOW_API_KEY")
RAGFLOW_URL = "http://127.0.0.1:9380"
