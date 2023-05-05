class LoginRequest:
    def __init__(self, name, password):
        self.name = name
        self.password = password

    @staticmethod
    def from_json(json):
        return LoginRequest(
            json.get("name", ""),
            json.get("password", ""),
        )