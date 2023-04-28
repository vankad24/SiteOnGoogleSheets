from server.response.BaseResponse import BaseResponse


class AllTitlesResponse(BaseResponse):
    def __init__(self, titles):
        super().__init__()
        arr = []
        for i, title in enumerate(titles):
            if title is not None:
                arr.append({"id":i+1,"title":title})
        self.body["titles"] = arr