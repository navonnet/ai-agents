import os
import json
from dotenv import load_dotenv
import requests

class NotifyMe():
    def __init__(self) -> None:
        self.pushUrl = os.getenv("PUSHOVER_URL")

    def notify(self, message):
        requests.post(self.pushUrl, data={
            "token": os.getenv("PUSHOVER_TOKEN"),
            "user": os.getenv("PUSHOVER_USER"),
            "message": message,
        })