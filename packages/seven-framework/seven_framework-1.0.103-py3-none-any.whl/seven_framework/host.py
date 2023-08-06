# -*- coding: utf-8 -*-
"""
@Author: ChenXiaolei
@Date: 2020-04-26 14:11:31
@LastEditTime: 2020-05-28 11:23:16
@LastEditors: ChenXiaolei
@Description: 
"""
import socket


class HostHelper:
    @classmethod
    def get_host_ip(self):
        """
        查询本机ip地址
        :return: ip
        """
        ip = ""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('114.114.114.114', 80))
            ip = s.getsockname()[0]
        except:
            pass
        finally:
            s.close()

        return ip
