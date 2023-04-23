from server.response.BaseResponse import BaseResponse


class AllTitlesResponse(BaseResponse):
    def __init__(self, ids, titles):
        super().__init__()
        arr = []
        for i in range(len(ids)):
            arr.append({"id":ids[i],"title":titles[i]})
        self.body["titles"] = arr
