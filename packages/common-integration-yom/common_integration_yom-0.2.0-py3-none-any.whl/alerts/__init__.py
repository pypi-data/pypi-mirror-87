import json
import sys
import random
import requests
import time

class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls)\
                .__call__(*args, **kwargs)
        return cls._instances[cls]


class Slack(metaclass=Singleton):
    def __init__(self, web_hook):
        self.web_hook = web_hook

    def send_alert(self, title, message):
        url = self.web_hook
        message = message
        title = title
        ts = time.time()
        slack_data = {
            "username": "NotificationBot",
            "icon_emoji": ":satellite:",
            "channel" : "#integration-alerts",
            "author_icon": "https://www.youorder.me/assets/icons/ic_logo_footer.svg",
            "attachments": [
                {
                    "color": "#9733EE",
                    "title": title,
                    "text": message,
                    "footer": "Integrations YOM",
                    "footer_icon": "https://www.youorder.me/assets/icons/ic_logo_footer.svg",
                    "ts": ts,
                }
            ]
        }
        byte_length = str(sys.getsizeof(slack_data))
        headers = {'Content-Type': "application/json", 'Content-Length': byte_length}
        response = requests.post(url, data=json.dumps(slack_data), headers=headers)
        if response.status_code != 200:
            raise Exception(response.status_code, response.text)
