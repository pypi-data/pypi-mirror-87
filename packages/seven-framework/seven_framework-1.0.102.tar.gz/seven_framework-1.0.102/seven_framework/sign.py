# -*- coding: utf-8 -*-
"""
@Author: ChenXiaolei
@Date: 2020-08-24 16:50:09
@LastEditTime: 2020-08-24 16:51:06
@LastEditors: ChenXiaolei
@Description: 
"""
import hashlib

class SignHelper(object):
    """ 
    @description: 签名工具类
    """

    @classmethod
    def params_sign_md5(self, params=None, app_key=None):
        """
        @description: 生成签名工具
        @param params: 必要参数，为字典格式
        @param  app_key: 应用密钥
        @return sign: 签名 
        @last_editors: LinGuilin
        """

        # 所有参数生成字典
        sign_params = {}
        for k, v in params.items():
            if not v or v == "":
                continue
            sign_params[k] = v
        params_sorted = sorted(sign_params.items(),
                               key=lambda e: e[0],
                               reverse=False)
        message = "".join(u"{}".format(v)for k, v in params_sorted)

        # MD5摘要
        encrypt = hashlib.md5()
        encrypt.update((message+str(app_key)).encode("utf-8"))
        sign = encrypt.hexdigest().lower()
        return sign
