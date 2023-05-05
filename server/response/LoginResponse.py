from server.model.User import User
from server.response.BaseResponse import BaseResponse


class LoginResponse(BaseResponse):
    def __init__(self, user: User):
        super().__init__()
        self.body["token"] = user.token
        self.body["name"] = user.name
        self.body["id"] = user.uid
