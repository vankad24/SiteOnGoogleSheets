import base64
import json

from googleapiclient.errors import HttpError

from server.repository.PostRepository import PostRepository
from server.data.DataSource import SpreadSheet
from server.model.ApiException import ApiException
from server.request.AddPostRequest import AddPostRequest
from server.request.ChangePostRequest import ChangePostRequest
from server.request.GetPostRequest import GetPostRequest
from server.response.AddPostResponse import AddPostResponse
from server.response.AllTitlesResponse import AllTitlesResponse
from server.response.BaseResponse import BaseResponse
from server.response.ErrorResponse import ErrorResponse
from server.response.GetPostResponse import GetPostResponse

dataSource = SpreadSheet()
postRep = PostRepository(dataSource.open_sheet("Posts"))
# userRep = UserRepository(dataSource.open_sheet("Users"))

def json_from_event(event):
    body = event["body"]
    if event["isBase64Encoded"]:
        body = base64.b64decode(body)
    json_obj = json.loads(body)
    return json_obj

def respond(response: BaseResponse):
    return response.to_dict()

def handler(event, context):
    try:
        #json_obj is a simple python dict
        json_obj = json_from_event(event)
    except Exception as e:
        return respond(ErrorResponse("Parse json exception: "+e.args[0]))

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

    try:
        resp = endpoint(json_obj)
    except ApiException as e:
        resp = ErrorResponse(e.msg)
    except HttpError as e:
        resp = ErrorResponse("Google Sheets:"+e.args[0])
    return respond(resp)


def get_all_titles(json_obj):
    titles = postRep.get_column_titles()
    return AllTitlesResponse(titles)

def get_post(json_obj):
    req = GetPostRequest.from_json(json_obj)
    post = postRep.get_post_by_id(req.id)
    return GetPostResponse(post)

def add_new_post(json_obj):
    req = AddPostRequest.from_json(json_obj)
    post_id = postRep.add_post(req.title, req.content)
    return AddPostResponse(post_id)

def change_content(json_obj):
    req = ChangePostRequest.from_json(json_obj)
    post = postRep.get_post_by_id(req.id)
    post.content = req.content
    postRep.change_post(post)
    return BaseResponse()

def change_title(json_obj):
    req = ChangePostRequest.from_json(json_obj)
    post = postRep.get_post_by_id(req.id)
    post.title = req.title
    postRep.change_post(post)
    return BaseResponse()

def delete_post(json_obj):
    req = GetPostRequest.from_json(json_obj)
    postRep.delete_post_by_id(req.id)
    return BaseResponse()


#for local tests
if __name__ == "__main__":
    test_body = {
        "action":"change_content",
        "id":5,
        "title":"New title",
        "content": "New content"
    }
    test_event = {
        "isBase64Encoded": False,
        "body": str(test_body).replace("'",'"')
    }
    print(handler(test_event, None))
