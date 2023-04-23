import json
import base64

class BaseRequest:
    def __init__(self, json_obj):
        pass

    @staticmethod
    def from_event(event):
        body = event["body"]
        if event["isBase64Encoded"]:
            body = base64.b64decode(body)
        json_obj = json.loads(body)
        return BaseRequest(
            json_obj
        )

