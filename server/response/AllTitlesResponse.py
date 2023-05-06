from server.response.BaseResponse import BaseResponse


class AllTitlesResponse(BaseResponse):
    def __init__(self, titles, heads):
        super().__init__()
        arr = []
        l = len(heads)
        for i, title in enumerate(titles):
            if title is not None:
                h = "" if i>=l or heads[i] is None else heads[i]
                arr.append({"id":i+1,"title":title,"head":h})
        self.body["titles"] = arr