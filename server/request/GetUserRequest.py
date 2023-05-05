class GetUserRequest:
    def __init__(self, uid):
        self.id = uid

    @staticmethod
    def from_json(json):
        return GetUserRequest(
            json.get("id", ""),
        )