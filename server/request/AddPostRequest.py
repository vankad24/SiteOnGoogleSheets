class AddPostRequest:
    def __init__(self, title, content, token):
        self.token = token
        self.content = content
        self.title = title

    @staticmethod
    def from_json(json):
        return AddPostRequest(
            json.get("title", ""),
            json.get("content", ""),
            json.get("token", "")
        )