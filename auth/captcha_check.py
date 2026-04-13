import requests
import sys
import json

SMARTCAPTCHA_SERVER_KEY = ""

def check_captcha(token, addr):
    resp = requests.post(
       "https://smartcaptcha.cloud.yandex.ru/validate",
       data={
          "secret": SMARTCAPTCHA_SERVER_KEY,
          "token": token,
          "ip": addr
       },
       timeout=1
    )
    server_output = resp.content.decode()
    if resp.status_code != 200:
       print(f"Allow access due to an error: code={resp.status_code}; message={server_output}", file=sys.stderr)
       return True
    return json.loads(server_output)["status"] == "ok"
