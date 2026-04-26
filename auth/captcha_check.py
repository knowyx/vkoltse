# This module contains functions for checking captcha, it uses Yandex SmartCaptcha service for this purpose, it sends a request to the service with the token received from the client and the client's IP address, and checks the response from the service to determine if the captcha is valid or not
import json
import sys

import requests

SMARTCAPTCHA_SERVER_KEY = ""


def check_captcha(token, addr):
    resp = requests.post(
        "https://smartcaptcha.cloud.yandex.ru/validate",
        data={"secret": SMARTCAPTCHA_SERVER_KEY, "token": token, "ip": addr},
        timeout=1,
    )
    server_output = resp.content.decode()
    if resp.status_code != 200:
        print(
            f"Allow access due to an error: code={resp.status_code}; message={server_output}",
            file=sys.stderr,
        )
        return True
    return json.loads(server_output)["status"] == "ok"
