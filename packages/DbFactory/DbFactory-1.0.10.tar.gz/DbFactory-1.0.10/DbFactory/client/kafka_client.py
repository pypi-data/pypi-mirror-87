# coding:utf-8
# author caturbhuja
# date   2020/9/7 3:06 下午 
# wechat chending2012
# python pack
import traceback

# third part pack

# self pack
from .db_base import config
from .kafka_client_base import KafkaClientBase
from DbFactory.util.decorator import cost_time, time_out, try_and_reconnect


class KafkaClient:
    def __init__(self, **kwargs):
        self.client__ = KafkaClientBase(**kwargs)

    @cost_time(warning_time=config.get("ACTION_WARNING_TIME", 10), log=config.get("SELF_LOG"))
    @time_out(
        interval=config.get("ACTION_TIME_OUT", 120), log=config.get("SELF_LOG"),
        use_time_out_decorator=config.get("use_time_out_decorator")
    )
    def generation_func(self, method, *args, **kwargs):
        """建立反射， 重试机制位置，要求 client 内不要有 try cache"""
        def action():
            return getattr(self.client__, method)(*args, **kwargs)

        return try_and_reconnect(self.client__, action)
