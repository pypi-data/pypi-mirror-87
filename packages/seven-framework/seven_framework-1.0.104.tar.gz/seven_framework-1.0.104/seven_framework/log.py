# -*- coding: utf-8 -*-
"""
@Author: ChenXiaolei
@Date: 2020-04-16 21:32:43
@LastEditTime: 2020-07-08 10:28:09
@LastEditors: ChenXiaolei
@Description: 
"""

import logging
import logging.handlers
import time
import os
import json
import socket
import platform

from .mysql import *


class Logger:
    """
    指定保存日志的文件路径，日志级别，以及调用文件 将日志存入到指定的文件中
    级别优先级:NOTSET < DEBUG < INFO < WARNING < ERROR < CRITICAL
    """

    def __init__(self, log_file_name, log_level, logger, host_ip="", project_name=None, db_connect=None, db_table_name="python_log_tb"):
        """
        @description: 
        @param log_file_name: 日志存储文件路径
        @param log_level: 日志等级
        @param logger: 日志标识
        @param host_ip: 服务器IP
        @param project_name: 项目标志
        @last_editors: ChenXiaolei
        """
        if not project_name:
            if platform.system() == "Windows":
                project_name = os.getcwd().split('\\')[-1]
            else:
                project_name = os.getcwd().split('/')[-1]

        # 判断文件夹是否存在，不存在则创建
        path_list = log_file_name.split("/")
        path_log = log_file_name[0:log_file_name.find(path_list[len(path_list)
                                                                - 1])]
        if not os.path.isdir(path_log):
            os.mkdir(path_log)

        logging_level = ''

        if log_level.upper() == 'NOTSET':
            logging_level = logging.NOTSET
        elif log_level.upper() == 'DEBUG':
            logging_level = logging.DEBUG
        elif log_level.upper() == 'INFO':
            logging_level = logging.INFO
        elif log_level.upper() == 'WARNING':
            logging_level = logging.WARNING
        elif log_level.upper() == 'ERROR':
            logging_level = logging.ERROR
        elif log_level.upper() == 'CRITICAL':
            logging_level = logging.CRITICAL

        # 创建一个logger
        self.logger = logging.getLogger(logger)
        self.logger.setLevel(logging_level)

        # 创建handler，用于写入日志文件
        self.handler_file = logging.handlers.TimedRotatingFileHandler(
            log_file_name, 'D', 1, 10)
        # 设置 切分后日志文件名的时间格式 默认 log_file_name+"." + suffix 如果需要更改需要改logging 源码
        self.handler_file.suffix = "%Y%m%d.log"
        self.handler_file.setLevel(logging_level)

        formatter = logging.Formatter(
            json.dumps({
                "record_time": "%(asctime)s",
                "level": "%(levelname)s",
                "log_msg": "%(message)s",
                "host_ip": host_ip,
                "project_name": project_name
            }))
        self.handler_file.setFormatter(formatter)

        # 创建handler，用于输出至控制台
        # 定义控制台输出handler的输出格式
        formatter = logging.Formatter(
            '[%(asctime)s][%(name)s][%(levelname)s]%(message)s')
        self.handler_console = logging.StreamHandler()  # 输出到控制台的handler
        self.handler_console.setFormatter(formatter)

        # 给logger添加handler
        if not self.logger.handlers:
            self.logger.addHandler(self.handler_file)
            self.logger.addHandler(self.handler_console)

        if db_connect:
            self.handler_db = LoggerMysqlHandler(
                db_connect, db_table_name, project_name, host_ip)
            self.logger.addHandler(self.handler_db)

    def close(self):
        self.logger.removeHandler(self.handler_file)
        self.handler_file.close()

        if hasattr(self, "handler_console"):
            self.logger.removeHandler(self.handler_console)
            self.handler_console.close()
        if hasattr(self, "handler_db"):
            self.logger.removeHandler(self.handler_db)
            self.handler_db.close()

    def get_logger(self):
        return self.logger

    @classmethod
    def get_logger_by_name(self, loger_name):
        """
        @description: 通过日志标识获取logger
        @param loger_name: 日志标识
        @return: logger
        @last_editors: ChenXiaolei
        """
        return logging.getLogger(loger_name)


class LoggerMysqlHandler(logging.Handler):
    def __init__(self, db_connect, table_name, project_name="", host_ip=""):
        try:
            if not db_connect:
                raise "未配置日志传输数据库配置"
                return
            self.db = MySQLHelper(db_connect)
            self.table_name = table_name
            self.project_name = project_name
            self.host_ip = host_ip
            # 判断制定数据库中标是否存在
            exist_result = self.db.fetch_one_row(
                f"SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA='{db_connect['db']}' AND TABLE_NAME='{table_name}';")

            if not exist_result:
                self.db.fetch_and_commit(
                    f"CREATE TABLE `{table_name}` ( `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键id', `project_name` varchar(50) DEFAULT NULL COMMENT '项目名称', `level` varchar(20) DEFAULT NULL COMMENT '日志等级', `host_ip` varchar(50) DEFAULT NULL COMMENT '服务器ip', `record_time` datetime NOT NULL COMMENT '记录时间', `record_timestamp` int(11) NOT NULL COMMENT '记录时间',`log_msg` longtext NOT NULL COMMENT '日志内容', PRIMARY KEY (`id`) ) ENGINE=InnoDB DEFAULT CHARSET=utf8;")
            logging.Handler.__init__(self)
        except Exception as ex:
            print(ex)
            pass

    def emit(self, record):
        try:
            self.db.fetch_and_commit(
                f"INSERT INTO {self.table_name}(project_name,level,host_ip,record_time,record_timestamp,log_msg) VALUE('{self.project_name}','{record.levelname}','{self.host_ip}','{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(record.created)))}',{int(record.created)},'{pymysql.escape_string(record.message)}');")
        except Exception as ex:
            print(ex)
            pass
