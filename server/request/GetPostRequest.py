class GetPostRequest:
    def __init__(self, pid):
        self.id = pid

    @staticmethod
    def from_json(json):
        return GetPostRequest(json.get("id", -1))