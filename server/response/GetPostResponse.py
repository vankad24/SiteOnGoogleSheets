from server.response.BaseResponse import BaseResponse


class GetPostResponse(BaseResponse):
    def __init__(self, post):
        super().__init__()
        self.body["post"] = post.to_dict()
