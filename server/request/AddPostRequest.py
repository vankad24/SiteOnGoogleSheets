class AddPostRequest:
    def __init__(self, title, content):
        self.content = content
        self.title = title

    @staticmethod
    def from_json(json):
        return AddPostRequest(
            json.get("title", ""),
            json.get("content", ""),
        )