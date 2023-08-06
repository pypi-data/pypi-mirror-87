# -*- coding: utf-8 -*-
"""
@Author: ChenXiaolei
@Date: 2020-03-06 23:17:54
@LastEditTime: 2020-12-04 14:25:37
@LastEditors: ChenXiaolei
@Description: Handler基础类
"""

# base import
import tornado.web
import time
import datetime
import base64
import json
import io
import bleach
import asyncio
import traceback

# tornado import
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor

# seven_framework import
from seven_framework import *


class BaseHandler(tornado.web.RequestHandler):
    THREAD_POOL_COUNT = 500
    """
    @description: 基础handler
    @last_editors: ChenXiaolei
    """
    executor = ThreadPoolExecutor(THREAD_POOL_COUNT)

    def __init__(self, *argc, **argkw):
        """
        @description: 初始化
        @last_editors: ChenXiaolei
        """
        super(BaseHandler, self).__init__(*argc, **argkw)
        self.logger_error = Logger.get_logger_by_name("log_error")
        self.logger_info = Logger.get_logger_by_name("log_info")

    # 异步重写
    async def get(self, *args, **kwargs):
        await asyncio.get_event_loop().run_in_executor(self.executor,
                                                       self.get_async)

    async def post(self, *args, **kwargs):
        await asyncio.get_event_loop().run_in_executor(self.executor,
                                                       self.post_async)

    async def delete(self, *args, **kwargs):
        await asyncio.get_event_loop().run_in_executor(self.executor,
                                                       self.delete_async)

    async def put(self, *args, **kwargs):
        await asyncio.get_event_loop().run_in_executor(self.executor,
                                                       self.put_async)

    async def head(self, *args, **kwargs):
        await asyncio.get_event_loop().run_in_executor(self.executor,
                                                       self.head_async)

    async def options(self, *args, **kwargs):
        await asyncio.get_event_loop().run_in_executor(self.executor,
                                                       self.options_async)

    def prepare(self, *argc, **argkw):
        """
        @description: 置于任何请求方法前被调用(请勿重写此函数,可重写prepare_ext)
        @last_editors: ChenXiaolei
        """
        try:
            if "Content-Type" in self.request.headers and self.request.headers[
                    "Content-type"].lower().find(
                        "application/json") >= 0 and self.request.body:
                request_params = json.loads(self.request.body)
            else:
                request_params = self.request.arguments
            http_request = dict(
                request_time=TimeHelper.get_now_format_time(),
                expend_time=self.request.request_time(),
                response_time=TimeHelper.get_now_format_time(),
                request_ip=self.get_remote_ip(),
                method=self.request.method,
                url=self.request.uri,
                request_params=request_params,
                http_status_code=self.get_status(),
            )

            http_request_msg = f"http_request:{json.dumps(http_request,ensure_ascii=False, cls=JsonEncoder)}"

            http_log = config.get_value("http_log")
            if http_log and http_log == True:
                self.logger_info.info(http_request_msg)
            else:
                print('\033[33m' + http_request_msg + '\033[0m')

            self.prepare_ext()
        except Exception as ex:
            self.logger_error.error(traceback.format_exc())

    def prepare_ext(self):
        """
        @description: 置于任何请求方法前被调用扩展
        @last_editors: ChenXiaolei
        """
        pass

    def render(self, template_name, **template_vars):
        """
        @description: 渲染html源码
        @param template_name: 前端模板路径
        @param **template_vars: 传递给模板的参数
        @return: 返回客户端渲染页面
        @last_editors: ChenXiaolei
        """
        html = self.render_string(template_name, **template_vars)
        self.write(html)

    def request_body_to_entity(self, model_entity):
        """
        @description: 表单数据对应到实体对象
        @param model_entity: 数据模型类
        @return: 装载model_entity 装载成功True 失败False
        @last_editors: ChenXiaolei
        """
        field_list = model_entity.get_field_list()
        for field_str in field_list:
            try:
                if str(field_str).lower() in ["id"]:
                    continue
                if field_str in self.request.arguments:
                    field_val = self.get_argument(field_str)
                    if field_val is not None:
                        setattr(model_entity, field_str,
                                self.html_clean(field_val))
            except Exception as exp:
                return False
        return True

    def request_body_to_dict(self):
        """
        @description: body参数转字典
        @return: 参数字典
        @last_editors: ChenXiaolei
        """
        dict_body = {}
        if self.request.body:
            dict_str = str.split(
                CodingHelper.url_decode(
                    self.request.body.decode("unicode_escape'")), "&")
            for item in dict_str:
                kv = str.split(item, "=")
                dict_body[kv[0]] = kv[1]
        return dict_body

    def check_xsrf_cookie(self):
        """
        @description: 过滤受_xsrf影响的post请求 通过获取_xsrf|X-Xsrftoken|X-Csrftoken判断
        @last_editors: ChenXiaolei
        """
        def _time_independent_equals(a, b):
            if len(a) != len(b):
                return False
            result = 0
            if isinstance(a[0], int):  # python3 byte strings
                for x, y in zip(a, b):
                    result |= x ^ y
            else:  # python2
                for x, y in zip(a, b):
                    result |= ord(x) ^ ord(y)
            return result == 0

        if '/api/' in self.request.uri:
            return
        else:
            token = (self.get_argument("_xsrf", None)
                     or self.request.headers.get("X-Xsrftoken")
                     or self.request.headers.get("X-Csrftoken"))
            if not token:
                raise tornado.web.HTTPError(
                    403, "'_xsrf' argument missing from POST")
            _, token, _ = self._decode_xsrf_token(token)
            _, expected_token, _ = self._get_raw_xsrf_token()
            if not _time_independent_equals(
                    tornado.web.escape.utf8(token),
                    tornado.web.escape.utf8(expected_token)):
                raise tornado.web.HTTPError(
                    403, "XSRF cookie does not match POST argument")

    # 页面过滤方法，防止注入
    def html_clean(self, htmlstr):
        """
           采用bleach来清除不必要的标签，并linkify text
        """
        tags = [
            'a', 'abbr', 'acronym', 'b', 'blockquote', 'code', 'em', 'i', 'li',
            'ol', 'strong', 'ul'
        ]
        tags.extend([
            'div', 'p', 'hr', 'br', 'pre', 'code', 'span', 'h1', 'h2', 'h3',
            'h4', 'h5', 'del', 'dl', 'img', 'sub', 'sup', 'u'
            'table', 'thead', 'tr', 'th', 'td', 'tbody', 'dd', 'caption',
            'blockquote', 'section'
        ])
        attributes = {
            '*': ['class', 'id'],
            'a': ['href', 'title', 'target'],
            'img': ['src', 'style', 'width', 'height']
        }
        return bleach.linkify(
            bleach.clean(htmlstr, tags=tags, attributes=attributes))

    def write_error(self, status_code, **kwargs):
        """
        @description: 重写全局异常事件捕捉
        @last_editors: ChenXiaolei
        """
        self.logger_error.error(traceback.format_exc())

    def get_param(self, param_name, default="", strip=True):
        """
        @description: 二次封装获取参数
        @param param_name: 参数名
        @param default: 如果无此参数，则返回默认值
        @return: 参数值
        @last_editors: ChenXiaolei
        """
        param_ret = self.get_argument(param_name, default, strip=strip)
        if param_ret == "":
            param_ret = default
        return param_ret

    def get_remote_ip(self):
        """
        @description: 获取客户端真实IP
        @return: 客户端真实IP字符串
        @last_editors: ChenXiaolei
        """
        ip_address = ""
        if "X-Forwarded-For" in self.request.headers:
            ip_address = self.request.headers['X-Forwarded-For']
        elif "X-Real-Ip" in self.request.headers:
            ip_address = self.request.headers['X-Real-Ip']
        else:
            ip_address = self.request.remote_ip
        return ip_address

    def reponse_common(self, result, desc, data=None):
        """
        @description: 输出公共json模型
        @param result: 返回结果标识
        @param desc: 返回结果描述
        @param data: 返回结果对象，即为数组，字典
        @return: 将dumps后的数据字符串返回给客户端
        @last_editors: ChenXiaolei
        """
        template_value = {}
        template_value['result'] = result
        template_value['desc'] = desc
        template_value['data'] = data

        self.http_reponse(
            json.dumps(template_value, ensure_ascii=False, cls=JsonEncoder))

    def http_reponse(self, content):
        """
        @description: 将字符串返回给客户端
        @param content: 内容字符串
        @return: 将字符串返回给客户端
        @last_editors: ChenXiaolei
        """
        http_log = config.get_value("http_log")
        content_log_info = f"公共返回:{content}"
        if http_log and http_log == True:
            self.logger_info.info(content_log_info)
        else:
            print('\033[34m' + content_log_info + '\033[0m')
        self.write(content)

    def reponse_json_success(self, data=None, desc='success'):
        """
        @description: 通用成功返回json结构
        @param data: 返回结果对象，即为数组，字典
        @param desc: 返回结果描述
        @return: 将dumps后的数据字符串返回给客户端
        @last_editors: ChenXiaolei
        """
        self.reponse_common(1, desc, data)

    def reponse_json_error(self, desc='error'):
        """
        @description: 通用错误返回json结构
        @param desc: 返错误描述
        @return: 将dumps后的数据字符串返回给客户端
        @last_editors: ChenXiaolei
        """
        self.reponse_common(0, desc)

    def reponse_json_error_params(self, desc='params error'):
        """
        @description: 通用参数错误返回json结构
        @param desc: 返错误描述
        @return: 将dumps后的数据字符串返回给客户端
        @last_editors: ChenXiaolei
        """
        self.reponse_common(0, desc)

    def redirect_url(self,
                     url: str,
                     permanent: bool = False,
                     status: int = None):
        """
        @description: 用于异步handler直接进行页面重定向
        @param url: 需跳转到的url
        @param permanent: 表示该重定向为临时性的；如果为True，则该重定向为永久性。
        @param status: 默认302,当status被指定了值的话，那个该值将会作为HTTP返回给客户端的状态码；如果没有指定特定的值，那么根据上方的permanent状态，如果permanent为True，则该status返回301；如果permanent为False，则该status返回302。
        @return: 重定向
        @last_editors: ChenXiaolei
        """
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        self.redirect(url, permanent, status)


def filter_check_params(must_params=None):
    """
    @description: 参数过滤装饰器 仅限handler使用,
                  提供参数的检查及获取参数功能
                  装饰器使用方法:
                  @filter_check_params("param_a,param_b,param_c")  或
                  @filter_check_params(["param_a","param_b,param_c"])
                  参数获取方法:
                  self.request_params[param_key]
    @param must_params: 必须传递的参数集合
    @last_editors: ChenXiaolei
    """
    def check_params(handler):
        def wrapper(self, **args):
            self.request_params = {}
            if type(must_params) == str:
                must_array = must_params.split(",")
            if type(must_params) == list:
                must_array = must_params
            if "Content-Type" in self.request.headers and self.request.headers[
                    "Content-type"].lower().find(
                        "application/json") >= 0 and self.request.body:
                json_params = {}
                try:
                    json_params = json.loads(self.request.body)
                except:
                    self.reponse_json_error_params()
                    return
                if json_params:
                    for field in json_params:
                        self.request_params[field] = json_params[field]
            else:
                for field in self.request.arguments:
                    self.request_params[field] = self.get_param(field)
            if must_params:
                for must_param in must_array:
                    if not must_param in self.request_params or self.request_params[
                            must_param] == "":
                        self.reponse_json_error_params()
                        return
            return handler(self, **args)

        return wrapper

    return check_params
