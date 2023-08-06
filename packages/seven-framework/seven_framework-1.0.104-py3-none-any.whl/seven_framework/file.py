# -*- coding: utf-8 -*-
"""
@Author: ChenXiaolei
@Date: 2020-05-19 10:33:52
@LastEditTime: 2020-12-07 14:01:07
@LastEditors: ChenXiaolei
@Description: ufile传输
"""
from ufile.filemanager import *
import traceback


class UFileHelper(FileManager):
    def __init__(self,
                 public_key,
                 private_key,
                 bucket=None,
                 connection_timeout=300,
                 upload_suffix=None,
                 download_suffix=None,
                 expires=None,
                 user_agent=None,
                 md5=None,
                 cdn_prefix=None,
                 src_prefix=None):
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
        ufile.config.set_default(connection_timeout=connection_timeout,
                                 expires=expires,
                                 user_agent=user_agent,
                                 uploadsuffix=upload_suffix,
                                 downloadsuffix=download_suffix,
                                 md5=md5)

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
        ret, resp = self.putfile(self._get_bucket(bucket),
                                 put_key,
                                 localfile,
                                 header=header)

        result = {}

        if resp.status_code == 200:
            if hasattr(self, "src_prefix") and self.src_prefix != "":
                result["src_url"] = self.src_prefix.rstrip('/') + "/" + put_key
            else:
                result["src_url"] = "/" + put_key

            if hasattr(self, "cdn_prefix") and self.cdn_prefix != "":
                result["cdn_url"] = self.cdn_prefix.rstrip('/') + "/" + put_key
            else:
                result["cdn_url"] = "/" + put_key

        return result

    def download_file(self,
                      key,
                      localfile,
                      isprivate=False,
                      content_range=None,
                      header=None,
                      bucket=None):
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

        return super().download_file(bucket,
                                     key,
                                     localfile,
                                     isprivate=isprivate,
                                     content_range=content_range,
                                     header=header)


class KS3Helper():

    ACCESS_KEY = ''
    SECRET_KEY = ''
    REGION_ENDPOINT = ""

    def __init__(self, access_key, secret_key, host):
        from ks3.connection import Connection
        self.ACCESS_KEY = access_key
        self.SECRET_KEY = secret_key
        self.HOST = host
        self.KS3_CONNECTION = Connection(self.ACCESS_KEY,
                                         self.SECRET_KEY,
                                         host=self.HOST,
                                         is_secure=False,
                                         domain_mode=False)

    def get_file_info(self, bucket_name, key_name):
        """
        @description: 获取文件信息
        @param bucket_name: bucket名称
        @param key_name: 存储对象名称
        @return 文件信息  异常返回None
        @last_editors: ChenXiaolei
        """
        bucket = self.__get_bucket(bucket_name)
        try:
            key_info = bucket.get_key(key_name)
            return key_info
        except:
            raise

    def get_file_contents(self, bucket_name, key_name):
        """
        @description: 获取指定文件的字节流
        @param bucket_name: bucket名称
        @param key_name: 存储对象名称
        @return 文件字节流
        @last_editors: ChenXiaolei
        """
        bucket = self.__get_bucket(bucket_name)
        try:
            key = bucket.get_key(key_name)
            contents = key.get_contents_as_string().decode()
            print(contents)
            return contents
        except:
            raise

    def save_file(self, bucket_name, key_name, saved_file_path):
        """
        @description: 保存指定存储文件到本地
        @param bucket_name: bucket名称
        @param key_name: 存储对象名称
        @param saved_file_path: 保存文件的本地路径
        @return 成功返回True 失败抛出异常
        @last_editors: ChenXiaolei
        """
        bucket = self.__get_bucket(bucket_name)
        try:
            key = bucket.get_key(key_name)
            contents = key.get_contents_to_filename(saved_file_path)
            print(contents)
            return True
        except:
            raise

    def put_file_from_file_path(self,
                                bucket_name,
                                key_name,
                                source_file_path,
                                policy="public-read"):
        """
        @description: 
        @param bucket_name: bucket名称
        @param key_name: 存储对象名称
        @param source_file_contents: 本地文件路径
        #param policy: 文件政策 私有:'private'   公共读:'public-read'
        @return 成功True 失败抛出异常
        @last_editors: ChenXiaolei
        """
        try:
            bucket = self.__get_bucket(bucket_name)
            key = bucket.new_key(key_name)
            ret = key.set_contents_from_filename(source_file_path,
                                                 policy=policy)
            if ret and ret.status == 200:
                print("金山存储文件上传成功")
                return True
        except:
            raise

        return False

    def put_file_from_contents(self,
                               bucket_name,
                               key_name,
                               source_file_contents,
                               policy="public-read"):
        """
        @description: 通过文件流上传文件
        @param bucket_name: bucket名称
        @param key_name: 存储对象名称
        @param source_file_contents: 文件流字符串
        @return 成功True 失败False
        @last_editors: ChenXiaolei
        """
        try:
            bucket = self.__get_bucket(bucket_name)
            key = bucket.new_key(key_name)
            ret = key.set_contents_from_string(source_file_contents,
                                               policy=policy)
            if ret and ret.status == 200:
                print("金山存储文件上传成功")
                return True
        except:
            raise
        return False

    def del_file(
        self,
        bucket_name,
        key_name,
    ):
        """
        @description: 删除文件
        @param bucket_name: bucket名称
        @param key_name: 存储对象名称
        @return 成功True 失败抛出异常
        @last_editors: ChenXiaolei
        """
        try:
            bucket = self.__get_bucket(bucket_name)
            bucket.delete_key(key_name)
            return True
        except:
            raise

    def multi_put_file(self,
                       bucket_name,
                       key_name,
                       source_file_path,
                       thread_num=5,
                       retry_times=3):
        """
        @description: 分片上传
        @param bucket_name: bucket名称
        @param key_name: 存储对象名称
        @param source_file_path: 本地文件路径
        @param thread_num: 线程数量
        @param retry_times: 重试次数
        @return 成功返回True 异常抛出异常
        @last_editors: ChenXiaolei
        """
        import math
        import threadpool

        bucket = self.__get_bucket(bucket_name)
        f_size = os.stat(source_file_path).st_size
        mp = bucket.initiate_multipart_upload(key_name)
        if not mp:
            raise RuntimeError("%s init multiupload error" % key_name)
        print(f"{key_name} begin multipart upload,uploadid={mp.id}")
        chunk_size = 104857600
        chunk_count = int(math.ceil(f_size / float(chunk_size)))
        pool_args_list = []
        try:
            for i in range(chunk_count):
                offset = chunk_size * i
                bs = min(chunk_size, f_size - offset)
                part_num = i + 1
                pool_args_list.append(([
                    mp, source_file_path, key_name, offset, bs, part_num,
                    retry_times
                ], None))
            pool = threadpool.ThreadPool(thread_num)
            requests = threadpool.makeRequests(self.__upload_part_task,
                                               pool_args_list)
            [pool.putRequest(req) for req in requests]
            pool.wait()
            if len(multi_task_result) != chunk_count:
                raise RuntimeError(
                    "%s part miss,expect=%d,actual=%d" %
                    (key_name, chunk_count, len(multi_task_result)))
            for item in multi_task_result.keys():
                if not multi_task_result[item]:
                    raise RuntimeError("%s part upload has fail" % key_name)
            mp.complete_upload()
            print(f"{key_name} multipart upload success")
            return True
        except:
            print(f"{key_name} multipart upload fail")
            if mp:
                mp.cancel_upload()
            return False

    def __upload_part_task(self, mp, source_file_path, key_name, offset,
                           chunk_size, part_num, retry_times):
        """
        @description: 分片上传任务
        @last_editors: ChenXiaolei
        """
        from filechunkio import FileChunkIO
        global multi_task_result
        multi_task_result = {}
        cur_task_ret = False
        try:
            for i in range(retry_times):
                try:
                    with FileChunkIO(source_file_path,
                                     'rb',
                                     offset=offset,
                                     bytes=chunk_size) as fp:
                        mp.upload_part_from_file(fp, part_num=part_num)
                    cur_task_ret = True
                    print(f"{key_name} part {part_num} upload success")
                    break
                except:
                    print(
                        f"{key_name} part {part_num} fail,uploadid={mp.id},error={traceback.format_exc()}"
                    )
                    if i + 1 >= retry_times:
                        print(f"{key_name} part {part_num} upload fail")
                        raise

        except:
            cur_task_ret = False
        finally:
            multi_task_result[part_num] = cur_task_ret

    def get_bucket_objects(self, bucket_name, prefix=None):
        """
        @description: 列举Bucket内的文件或者目录
        @param bucket_name: bucket名称
        @param prefix: 指定前缀
        @return: 文件列表，目录列表
        @last_editors: ChenXiaolei
        """
        from ks3.prefix import Prefix
        from ks3.key import Key

        result_list = []
        result_dir = []

        try:
            bucket = self.__get_bucket(bucket_name)
            if prefix and prefix != "":
                keys = bucket.list(prefix=prefix)
            else:
                keys = bucket.list(delimiter='/')
            for key in keys:
                if isinstance(key, Key):
                    result_list.append(key.name)
                elif isinstance(key, Prefix):
                    result_dir.append(key.name)
        except:
            raise

        return result_list, result_dir

    def __get_bucket(self, bucket_name):
        """
        @description: 获取bucket
        @param bucket_name: bucket名称
        @return bucket对象
        @last_editors: ChenXiaolei
        """
        return self.KS3_CONNECTION.get_bucket(bucket_name)