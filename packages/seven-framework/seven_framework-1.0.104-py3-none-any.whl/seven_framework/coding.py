# -*- coding: utf-8 -*-
"""
@Author: ChenXiaolei
@Date: 2020-05-11 21:46:17
@LastEditTime: 2020-05-25 16:29:57
@LastEditors: ChenXiaolei
@Description: 
"""

from urllib import parse


class CodingHelper():
    @classmethod
    def url_encode(self, text, coding='utf-8'):
        return parse.quote_plus(text, encoding='utf-8')

    @classmethod
    def url_decode(self, text, coding='utf-8'):
        return parse.unquote(text, 'utf-8')
