from server.response.BaseResponse import BaseResponse


class ErrorResponse(BaseResponse):
    def __init__(self, msg):
        super().__init__(False, {"message":msg})