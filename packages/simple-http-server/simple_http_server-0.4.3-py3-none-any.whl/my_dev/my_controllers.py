# -*- coding: utf-8 -*-

from simple_http_server import Redirect
from simple_http_server import Headers
from simple_http_server import StaticFile
from simple_http_server import HttpError
from simple_http_server import JSONBody
from simple_http_server import Header
from simple_http_server import Parameters
from simple_http_server import Cookie
from simple_http_server import Cookies
from simple_http_server import PathValue
from simple_http_server import Parameter
from simple_http_server import MultipartFile
from simple_http_server import Response
from simple_http_server import Request
from simple_http_server import filter_map
from simple_http_server import request_map
import os
import simple_http_server.logger as logger
import simple_http_server.server as server


__logger = logger.get_logger("my_test_main")


__logger = logger.get_logger("controller")


@request_map("/")
@request_map("/index")
def my_ctrl():
    return {"code": 0, "message": "success"}  # You can return a dictionary, a string or a `simple_http_server.simple_http_server.Response` object.


@request_map("/say_hello", method=["GET", "POST"])
def my_ctrl2(name, name2=Parameter("name", default="KEIJACK")):
    """name and name2 is the same"""
    return "<!DOCTYPE html><html><body>hello, %s, %s</body></html>" % (name, name2)


@request_map("/error")
def my_ctrl3():
    return Response(status_code=500)


@request_map("/exception")
def exception_ctrl():
    raise HttpError(400, "Exception")


@request_map("/upload", method="POST")
def my_upload(img=MultipartFile("img"), txt=Parameter("中文text", required=False, default="DEFAULT"), req=Request()):
    for k, v in req.parameter.items():
        print("%s (%s)====> %s " % (k, str(type(k)), v))
    print(txt)

    root = os.path.dirname(os.path.abspath(__file__))
    img.save_to_file(root + "/imgs/" + img.filename)
    return "<!DOCTYPE html><html><body>upload ok! %s </body></html>" % txt


@request_map("/post_txt", method=["GET", "POST"])
def normal_form_post(txt=Parameter("中文txt", required=False, default="DEFAULT"), req=Request()):
    for k, v in req.parameter.items():
        print("%s ====> %s " % (k, v))
    return "<!DOCTYPE html><html><body>hi, %s</body></html>" % txt


@request_map("/upload", method="GET")
def show_upload():
    root = os.path.dirname(os.path.abspath(__file__))
    return StaticFile("%s/my_test_index.html" % root, "text/html; charset=utf-8")


@request_map("/a.mov", method="GET")
def a_mov():
    return StaticFile("/home/keijack/Desktop/videos/inputs/a.mov")


@request_map("/post_json", method="POST")
def post_json(json=JSONBody()):
    print(json)
    return json


@request_map("/headers")
def set_headers(res=Response(), headers=Headers(), cookies=Cookies(), cookie=Cookie("sc")):
    print("==================cookies==========")
    print(cookies)
    print("==================cookies==========")
    print(cookie)
    res.add_header("Set-Cookie", "sc=keijack; Expires=Web, 31 Oct 2018 00:00:00 GMT;")
    res.add_header("Set-Cookie", "sc=keijack2;")
    res.body = "<!DOCTYPE html><html><body>OK!</body></html>"


@request_map("tuple")
def tuple_results():
    return 200, Headers({"my-header": "headers"}), {"success": "成功！"}


@request_map("tuple_cookie")
def tuple_with_cookies(headers=Headers(), all_cookies=Cookies(), cookie_sc=Cookie("sc")):
    print("=====>headers")
    print(headers)
    print("=====> cookies ")
    print(all_cookies)
    print("=====> cookie sc ")
    print(cookie_sc)
    print("======<")
    import datetime
    expires = datetime.datetime(2018, 12, 31)

    cks = Cookies()
    # cks = cookies.SimpleCookie() # you could also use the build-in cookie objects
    cks["ck1"] = "keijack"
    cks["ck1"]["path"] = "/"
    cks["ck1"]["expires"] = expires.strftime(Cookies.EXPIRE_DATE_FORMAT)

    return 200, Header({"xx": "yyy"}), cks, "<html><body>OK</body></html>"


@filter_map("^/tuple")
def filter_tuple(ctx):
    print("---------- through filter ---------------")
    # add a header to request header
    ctx.request.headers["filter-set"] = "through filter"
    if "user_name" not in ctx.request.parameter:
        ctx.response.send_redirect("/index")
    elif "pass" not in ctx.request.parameter:
        ctx.response.send_error(400, "pass should be passed")
        # you can also raise a HttpError
        # raise HttpError(400, "pass should be passed")
    else:
        # you should always use do_chain method to go to the next
        ctx.do_chain()


@request_map("/redirect")
def redirect():
    return Redirect("/index")


@request_map("/stop")
def stop():
    server.stop()
    return {"stopped": True}

@request_map("/params")
def my_ctrl4(user_name,
             password=Parameter(name="passwd", required=True),
             remember_me=True,
             locations=[],
             json_param={},
             lcs=Parameters(name="locals", required=True),
             content_type=Header("Content-Type", default="application/json"),
             connection=Header("Connection"),
             headers=Headers()
             ):
    print("user_name: " + user_name)
    print("password: " + password)
    print("remember_me: " + str(remember_me))
    print("locaitons: " + str(locations))
    print("locals: " + str(lcs))
    print("json_param: " + str(json_param))
    print("content_type: " + content_type)
    print("connection: " + connection)
    print("Headers: " + str(headers))

    return {"hello": "world"}


@request_map("/int_status_code")
def return_int(status_code=200):
    return status_code


@request_map("/a/{pval}/{path_val}/x")
def my_path_val_ctr(val=PathValue("pval"), path_val=PathValue()):
    __logger.info("val is %s , path_val is %s" % (val, path_val))
    return "<html><body>%s, %s</body></html>" % (val, path_val)
