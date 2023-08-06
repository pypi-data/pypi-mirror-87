# -*- coding: utf-8 -*-
"""
@Author: ChenXiaolei
@Date: 2020-03-21 18:29:31
@LastEditTime: 2020-05-25 15:33:43
@LastEditors: ChenXiaolei
@Description: 
@FilePath: /python_base_framework/libs/seven_framework/config.py
"""

import os
import json

import threading
_lock = threading.Condition()


def init_config(path):
    """
    @description: 初始化配置文件
    @param path：配置文件路径，可使用物理路径或url
    @return: global app_config
    @last_editors: ChenXiaolei
    """    
    if path.lower().find("http://") > -1:
        import requests
        json_str = requests.get(path)
    else:
        with open(path, "r+", encoding="utf-8") as f:
            json_str = f.read()
    global app_config
    app_config = json.loads(json_str)


def set_value(key, value):
    """
    @description: 设置一个全局键值配置
    @param key:参数键名
    @param value:参数值
    @return: 无
    @last_editors: ChenXiaolei
    """    
    _lock.acquire()
    try:
        app_config[key] = value
    except:
        raise
    finally:
        _lock.release()


def get_value(key, default_value=None):
    """
    @description: 获得一个全局变量,不存在则返回默认值
    @param key:参数键名
    @param default_value:获取不到返回的默认值
    @return: 参数值
    @last_editors: ChenXiaolei
    """
    try:
        _lock.acquire()
        config_value = app_config[key]
    except KeyError:
        # print(f"config未获取key[{key}]的配置")
        config_value = default_value
    finally:
        _lock.release()

    return config_value