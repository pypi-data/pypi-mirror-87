# -*- coding: utf-8 -*-
"""
@Author: ChenXiaolei
@Date: 2020-05-19 10:33:52
@LastEditTime: 2020-06-02 10:36:35
@LastEditors: ChenXiaolei
@Description: ufile传输
"""
from ufile.filemanager import *
from ufile import multipartuploadufile
from io import BytesIO
# UCloud UFile


class UFileHelper(FileManager):

    def __init__(self, public_key, private_key, bucket=None, connection_timeout=300, upload_suffix=None, download_suffix=None, expires=None, user_agent=None, md5=None, cdn_prefix=None, src_prefix=None):
        """
        @description: 初始化 PutUFile 实例
        @param public_key: string类型, 账户API公私钥中的公钥
        @param private_key: string类型, 账户API公私钥中的私钥
        @param bucket: ufile空间名称
        @param connection_timeout: integer类型，网络请求超时时间
        @param upload_suffix: string类型，上传地址后缀
        @param download_suffix: string类型，下载地址后缀
        @param expires: integer类型，文件下载链接失效时间
        @param user_agent: string类型 user_agent
        @md5: 布尔类型，上传文件是否携带MD5
        @return: None，如果为非法的公私钥，则抛出ValueError异常
        """
        super(UFileHelper, self).__init__(public_key, private_key)
        self.public_key = public_key
        self.private_key = private_key
        self.bucket = bucket
        if cdn_prefix:
            self.cdn_prefix = cdn_prefix
        if src_prefix:
            self.src_prefix = src_prefix

        import ufile.config
        ufile.config.set_default(connection_timeout=connection_timeout, expires=expires,
                                 user_agent=user_agent, uploadsuffix=upload_suffix, downloadsuffix=download_suffix, md5=md5)

    def _get_bucket(self, bucket=None):
        """
        @description: 获取ufile bucket
        @param bucket: ufile空间名称
        @return: bucket
        @last_editors: ChenXiaolei
        """
        if bucket and bucket != "":
            return bucket
        elif hasattr(self, "bucket") and self.bucket != "":
            return self.bucket
        else:
            raise Exception("ufile bucket is not configured")

    def put_file(self, put_key, localfile, header=None, bucket=None):
        """
        @description: 上传文件至ufile
        @param put_key: string 类型，上传文件在空间中的名称
        @param localfile: string类型，本地文件名称
        @param header: dict类型，http 请求header，键值对类型分别为string，比如{'User-Agent': 'Google Chrome'}
        @param bucket: string类型，上传空间名称 初始化参数和此函数参数二选一传递
        @return: 字典类型,包含源文件=>src_url和cdn文件=>cdn_url
        @last_editors: ChenXiaolei
        """
        ret, resp = self.putfile(self._get_bucket(
            bucket), put_key, localfile, header=header)

        result = {}

        if resp.status_code == 200:
            if hasattr(self, "src_prefix") and self.src_prefix != "":
                result["src_url"] = self.src_prefix.rstrip('/')+"/"+put_key
            else:
                result["src_url"] = "/"+put_key

            if hasattr(self, "cdn_prefix") and self.cdn_prefix != "":
                result["cdn_url"] = self.cdn_prefix.rstrip('/')+"/"+put_key
            else:
                result["cdn_url"] = "/"+put_key

        return result

    def download_file(self, key, localfile, isprivate=False, content_range=None, header=None, bucket=None):
        """
        下载UFile文件并且保存为本地文件

        @param key: string类型， 下载文件在空间中的名称
        @param localfile: string类型，要保存的本地文件名称
        @param isprivate: boolean类型，如果为私有空间则为True
        @param content_range: tuple类型，元素为两个整型
        @param header: dict类型，http 请求header，键值对类型分别为string，比如{'User-Agent': 'Google Chrome'}
        @param bucket: string类型, UFile空间名称
        @return: ret: 如果http状态码为[200, 204, 206]之一则返回None，否则如果服务器返回json信息则返回dict类型，键值对类型分别为string, unicode string类型，否则返回空的dict
        @return: ResponseInfo: 响应的具体信息，UCloud UFile 服务器返回信息或者网络链接异常
        """
        bucket = self._get_bucket(bucket)

        return super().download_file(bucket, key, localfile, isprivate=isprivate,  content_range=content_range, header=header)
