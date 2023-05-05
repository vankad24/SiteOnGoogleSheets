class ChangePostRequest:
    def __init__(self, pid, title, content,token):
        self.token = token
        self.content = content
        self.title = title
        self.id = pid

    @staticmethod
    def from_json(json):
        return ChangePostRequest(
            json.get("id", -1),
            json.get("title", ""),
            json.get("content", ""),
            json.get("token", "")
        )