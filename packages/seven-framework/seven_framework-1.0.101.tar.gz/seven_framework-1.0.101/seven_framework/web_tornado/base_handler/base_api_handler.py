# -*- coding: utf-8 -*-
"""
@Author: ChenXiaolei
@Date: 2020-03-06 23:17:54
@LastEditTime: 2020-05-27 16:30:11
@LastEditors: ChenXiaolei
@Description: Handler基础类
"""

# seven_framework import
from .base_handler import *


class BaseApiHandler(BaseHandler):
    """
    @description: api base handler. not session
    @last_editors: ChenXiaolei
    """

    def __init__(self, *argc, **argkw):
        """
        @description: 初始化
        @last_editors: ChenXiaolei
        """
        super(BaseApiHandler, self).__init__(*argc, **argkw)

    def write_error(self, status_code, **kwargs):
        """
        @description: 重写全局异常事件捕捉
        @last_editors: ChenXiaolei
        """
        self.logger_error.error(traceback.format_exc())
        return self.reponse_json_error()

    def prepare_ext(self):
        """
        @description: 置于任何请求方法前被调用扩展
        @last_editors: ChenXiaolei
        """
        pass
