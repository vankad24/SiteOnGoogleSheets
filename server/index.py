from server.model.ApiException import ApiException
from server.request.AddPostRequest import AddPostRequest
from server.request.ChangePostRequest import ChangePostRequest
from server.request.GetPostRequest import GetPostRequest
from server.response.AddPostResponse import AddPostResponse
from server.response.AllTitlesResponse import AllTitlesResponse
from server.response.BaseResponse import BaseResponse
from server.response.ErrorResponse import ErrorResponse
import json
import base64

from server.response.GetPostResponse import GetPostResponse

dataRep = DataRopository(SpreadSheet())

def json_from_event(event):
    body = event["body"]
    if event["isBase64Encoded"]:
        body = base64.b64decode(body)
    json_obj = json.loads(body)
    return json_obj

def respond(response: BaseResponse):
    return response.to_dict()

def handler(event, context):
    #json_obj is a simple python dict
    json_obj = json_from_event(event)
    if "action" not in json_obj:
        return respond(ErrorResponse("Action parameter required"))
    action = json_obj["action"]
    match action:
        case "get_all_titles":
            endpoint = get_all_titles
        case "add_new_post":
            endpoint = add_new_post
        case "get_post":
            endpoint = get_post
        case "change_title":
            endpoint = change_title
        case "change_content":
            endpoint = change_content
        case "delete_post":
            endpoint = delete_post
        case _:
            return respond(ErrorResponse("Wrong action"))
    return endpoint(json_obj)

# test
def get_all_titles(json_obj):
    # req = .from_json(json_obj)
    try:
        ids = dataRep.get_column_ids()
        titles = dataRep.get_column_titles()
        return respond(AllTitlesResponse(ids, titles))
    except ApiException as e:
        return respond(ErrorResponse(e.msg))
    #todo HttpException

def get_post(json_obj):
    req = GetPostRequest.from_json(json_obj)
    try:
        post = dataRep.get_post_by_id(req.id)
        return respond(GetPostResponse(post))
    except ApiException as e:
        return respond(ErrorResponse(e.msg))

def add_new_post(json_obj):
    req = AddPostRequest.from_json(json_obj)
    try:
        post_id = dataRep.add_post(req.title, req.content)
        return respond(AddPostResponse(post_id))
    except ApiException as e:
        return respond(ErrorResponse(e.msg))

def change_content(json_obj):
    req = ChangePostRequest.from_json(json_obj)
    try:
        post = dataRep.get_post_by_id(req.id)
        post.content = req.content
        dataRep.change_post(post)
        return respond(BaseResponse())
    except ApiException as e:
        return respond(ErrorResponse(e.msg))

def change_title(json_obj):
    req = ChangePostRequest.from_json(json_obj)
    try:
        post = dataRep.get_post_by_id(req.id)
        post.title = req.title
        dataRep.change_post(post)
        return respond(BaseResponse())
    except ApiException as e:
        return respond(ErrorResponse(e.msg))

def delete_post(json_obj):
    req = GetPostRequest.from_json(json_obj)
    try:
        dataRep.delete_post_by_id(req.id)
        return respond(BaseResponse())
    except ApiException as e:
        return respond(ErrorResponse(e.msg))


#for local tests
if __name__ == "__main__":
    test_body = {
        "action":"get_post",
        "id":3
    }
    test_event = {
        "isBase64Encoded": False,
        "body": str(test_body)
    }
    print(handler(test_event, None))