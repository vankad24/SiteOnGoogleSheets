from server.response.BaseResponse import BaseResponse


class AddPostResponse(BaseResponse):
    def __init__(self, post_id):
        super().__init__()
        self.body["id"] = post_id
