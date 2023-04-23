from server.request.BaseRequest import BaseRequest
from server.response.ApiException import ApiException
from server.response.BaseResponse import BaseResponse
from server.response.ErrorResponse import ErrorResponse


dataRep = DataRopository(DataSource())

def respond(response: BaseResponse):
    return response.to_dict()

   
def handler(event, context):
    req = BaseRequest.from_event(event)
    try:
        #dataRep.do_something(req.some_arg)
        return respond(BaseResponse())
    except ApiException as e:
        return respond(ErrorResponse(e.msg))