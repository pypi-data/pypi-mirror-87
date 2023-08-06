#!/usr/bin/env python
# -*- coding: utf-8 -*-
# wechat: chending2012

# python pack
import traceback
import time

# third part pack
import redis
# import leveldb

# self pack
from DbFactory.util.decorator import cost_time, time_out, try_and_reconnect
from .db_base import DbBase, config

"""
http://redisdoc.com/
redis 方法参考

todo 使用 leveldb 或者其他 生成本地缓存
"""


class RedisClient(DbBase):
    def __init__(self, **kwargs):
        super(RedisClient, self).__init__(**kwargs)
        self.client__ = None  # 统一规定 数据库实例使用这个名字
        if self.__class__.__name__ == "RedisClient":
            self.__init_db_base_args()
            self.__init_cache_args()
            self._reconnect()

    @property
    def origin_client(self):
        """
        实际上，redis不需要这个操作。
        可以直接给外部使用，这个不会享受 异常处理加成效果，需要被加成，则需要类似 mysql 一样，再封装一次
        """
        return self.client__

    def __init_db_base_args(self):
        """ 这里 填写一些默认的参数 """
        self._redis_ip = self._kwargs.pop('host', '0.0.0.0')
        self._redis_port = int(self._kwargs.pop('port', 6379))
        self._redis_db_name = int(self._kwargs.pop('db_name', 0))
        self._new_kwargs = {
            "host": self._redis_ip,
            "port": self._redis_port,
            "db": self._redis_db_name,
            "password": self._kwargs.pop('password', ''),
            "decode_responses": self._kwargs.pop('decode_responses', True),
            "socket_timeout": self._kwargs.pop('socket_timeout', 10),
        }
        self._new_kwargs = {**self._kwargs, **self._new_kwargs}

    def __init_cache_args(self):
        self._cache_time = self._kwargs.get('cache_time', 0)
        # self._leveldb_cache_dir = self._kwargs.get('leveldb_cache_dir')
        # self._is_cache = False
        # self._level_db_cache = None
        #
        # if self._cache_time > 0 and self._leveldb_cache_dir is not None:
        #     self._is_cache = True
        #     self._level_db_cache = leveldb.LevelDB(self._leveldb_cache_dir)
        #     self._cache_info = {}

    def _reconnect(self, count=0):
        try:
            self._log.info('=== redis kwargs is:{} ==='.format(self._new_kwargs))
            if self.client__:
                self.client__.close()
            self.client__ = redis.StrictRedis(**self._new_kwargs)
            self._log.info("redis connected success !")
        except Exception as e:
            count += 1
            self._log.error(
                "redis connecting error. retry times is {}, host: {}, port: {}, db: {}, err_msg: {}\t{}".format(
                    count, self._redis_ip, self._redis_port, self._redis_db_name, str(e), traceback.format_exc()))
            time.sleep(self._retry_sleep_time)
            self._reconnect(count)
    """
    核心方法，self.client__ 包含的方法，会被添加 异常处理功能。  目前，这里仅仅包含redis 本身自带功能，如果还需要封装，则需要类似mysql的方法，再封装一层。
    """

    @cost_time(warning_time=config.get("ACTION_WARNING_TIME", 5), log=config.get("SELF_LOG"))
    @time_out(
        interval=config.get("ACTION_TIME_OUT", 240), log=config.get("SELF_LOG"),
        use_time_out_decorator=config.get("use_time_out_decorator")
    )
    def generation_func(self, method, *args, **kwargs):
        def action():
            return getattr(self.client__, method)(*args, **kwargs)

        return try_and_reconnect(self.client__, action)
