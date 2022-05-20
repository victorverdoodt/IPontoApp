import requests
from config import Config


def send(to, subject, body, attachments=[]):
    data = {
        "apikey": Config.ELASTIC_EMAIL["APIKEY"],
        "subject": subject,
        "from": Config.ELASTIC_EMAIL["FROM_MAIL"],
        "fromName": Config.ELASTIC_EMAIL["FROM_NAME"],
        "to": to,
        "bodyHtml": body,
    }
    attachments = attachments if type(attachments) == list else [attachments]
    attachs = [(name, open(name, "rb")) for name in attachments]
    result = requests.post(
        Config.ELASTIC_EMAIL["URL"],
        params=data,
        files=attachs
    )
    result_json = result.json()
    if not result_json["success"]:
        return False, result_json["error"]
    return True, result_json["data"]