class GetPostRequest:
    def __init__(self, pid, token):
        self.token = token
        self.id = pid

    @staticmethod
    def from_json(json):
        return GetPostRequest(
            json.get("id", -1),
            json.get("token","")
        )