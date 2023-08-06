#!/usr/bin/env python
# -*- coding: utf-8 -*-
# wechat: chending2012

# python pack

# third part pack

# self pack
from DbFactory.util.decorator import cost_time, time_out, try_and_reconnect
from .db_base import config
from .mysql_client_base import MysqlClientBase


class MysqlClient:
    def __init__(self, **kwargs):
        self.client__ = MysqlClientBase(**kwargs)

    """
    核心方法，self.client__ 包含的方法，会被添加 异常处理功能。
    """

    @cost_time(warning_time=config.get("ACTION_WARNING_TIME", 10), log=config.get("SELF_LOG"))
    @time_out(
        interval=config.get("ACTION_TIME_OUT", 240), log=config.get("SELF_LOG"),
        use_time_out_decorator=config.get("use_time_out_decorator")
    )
    def generation_func(self, method, *args, **kwargs):
        """建立反射"""

        def action():
            return getattr(self.client__, method)(*args, **kwargs)

        return try_and_reconnect(self.client__, action)
