from server.model.User import User
from server.response.BaseResponse import BaseResponse


class GetUserResponse(BaseResponse):
    def __init__(self, user: User):
        super().__init__()
        self.body["name"] = user.name
        self.body["id"] = user.uid
