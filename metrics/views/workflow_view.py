import json


class WorkflowView(object):
    def __init__(self, status_code: int, body: dict):
        self.status_code = status_code
        self.body = json.dumps(body)

    def render(self):
        return {
            "body": self.body,
            "statusCode": self.status_code
        }