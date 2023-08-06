# -*- coding: utf-8 -*-
"""
@Author: ChenXiaolei
@Date: 2020-05-12 17:47:10
@LastEditTime: 2020-05-25 15:33:03
@LastEditors: ChenXiaolei
@Description: 基础tornado引用
"""
# 框架引用
import os
import tornado.web
import tornado.ioloop
import tornado.httpserver
import platform
from seven_framework import *
import sys
global environment
if "--production" in sys.argv:
    environment = "production"
    config_file = "config.json"
elif "--testing" in sys.argv:
    environment = "testing"
    config_file = "config_testing.json"
else:
    environment = "development"
    config_file = "config_dev.json"

sys.path.append(".local")  # 不可删除,置于其他import前
# 初始化配置,执行顺序需先于调用模块导入
config.init_config(config_file)  # 全局配置,只需要配置一次

# 初始化日志写入类调用方法
logger_error = None
logger_info = None
log_config = config.get_value("log")

if log_config and type(log_config) == dict and "db_log" in log_config:
    db_log = log_config["db_log"]
    db_log_table_name = log_config["db_log_table_name"] if "db_log_table_name" in log_config else "python_log_tb"
    log_info_to_db = log_config["log_info_to_db"] if "log_info_to_db" in log_config else True
    log_error_to_db = log_config["log_error_to_db"] if "log_error_to_db" in log_config else True

    if log_error_to_db:
        logger_error = Logger("logs/log_error", "ERROR", "log_error",
                              HostHelper.get_host_ip(), db_connect=db_log, db_table_name=db_log_table_name).get_logger()
    if log_info_to_db:
        logger_info = Logger("logs/log_info", "INFO", "log_info",
                             HostHelper.get_host_ip(), db_connect=db_log, db_table_name=db_log_table_name).get_logger()

if not logger_error:
    logger_error = Logger("logs/log_error", "ERROR", "log_error",
                          HostHelper.get_host_ip()).get_logger()
if not logger_info:
    logger_info = Logger("logs/log_info", "INFO", "log_info",
                         HostHelper.get_host_ip()).get_logger()