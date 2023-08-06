# coding:utf-8
# author caturbhuja
# date   2020/9/7 3:06 下午 
# wechat chending2012
# python pack
import time
import traceback
from functools import reduce, partial
import json
from DbFactory.util.bytes_decoder import decoder

# third part pack
from kafka import KafkaConsumer, TopicPartition, KafkaProducer, OffsetAndMetadata

# self pack
from .db_base import DbBase
from DbFactory.util.decorator import kafka_type_check

real_type = 'not None'


class KafkaClientBase(DbBase):
    def __init__(self, **kwargs):
        super(KafkaClientBase, self).__init__(**kwargs)

        self.singleton_sign = ''
        self.client__ = None
        self._topic = None
        self._partition = None

        self.__check_must_args()
        self.__init_db_base_args()
        self._reconnect()

    def __getattr__(self, item):
        return getattr(self.client__, item)

    def origin_client(self, singleton_sign):
        self.singleton_sign = singleton_sign
        return self.client__

    def __check_must_args(self):
        self._topic = self._kwargs.pop("topic", None)
        self._bootstrap_servers = self._kwargs.pop("bootstrap_servers", None)
        assert self._topic, "must be have topic"
        if not self._bootstrap_servers:
            self._log.warning('use localhost:9092 to kafka bootstrap_servers')
            self._bootstrap_servers = 'localhost:9092'

    def __init_db_base_args(self):
        """处理kafka基础参数"""
        self._init_type = self._kwargs.pop("init_type", 'consumer')
        self._partition = self._kwargs.pop("partition", None)
        self._enable_auto_commit = self._kwargs.pop("enable_auto_commit", True)
        self._args_dict = {
            "bootstrap_servers": self._bootstrap_servers
        }
        if self._init_type == 'consumer':
            self._args_dict["enable_auto_commit"] = self._enable_auto_commit
            self._args_dict["max_partition_fetch_bytes"] = int(self._kwargs.pop("max_partition_fetch_bytes", 6291456))
        else:
            self._args_dict["max_block_ms"] = int(self._kwargs.pop("max_block_ms", 2000))
            self._args_dict["batch_size"] = int(self._kwargs.pop("batch_size", 64384))
            self._args_dict["buffer_memory"] = int(self._kwargs.pop("buffer_memory", 640554432))
            self._args_dict["compression_type"] = self._kwargs.pop("compression_type", 'gzip')
            self._args_dict["linger_ms"] = int(self._kwargs.pop("linger_ms", 2000))

        self._hide_detail = self._kwargs.pop("hide_detail", True)
        self._auto_flush = self._kwargs.pop("auto_flush", True)

        self._group_id = self._kwargs.pop("group_id", None)
        if self._group_id:
            self._args_dict["group_id"] = self._group_id
        # 添加其他未处理的参数，可能会出现部分没有处理完成的函数，导致报错
        self._args_dict.update(self._kwargs)

    def _reconnect(self, count=0):
        """如果断开连接，则一直重试，直到成功"""
        global real_type
        self.close(timeout=10, info='when create connection')
        try:
            if self._init_type == 'consumer':
                self._log.info('=== kafka consumer kwargs is:{} ==='.format(self._args_dict))   # 部分日志不规范，无法打印
                print('=== kafka consumer kwargs is:{} ==='.format(self._args_dict))
                real_type = 'consumer'
                if self._partition is not None:
                    self.client__ = KafkaConsumer(**self._args_dict)
                    self.client__.assign([TopicPartition(self._topic, self._partition)])
                    self._log.info("init KafkaConsumer include partition success")
                else:
                    self.client__ = KafkaConsumer(self._topic, **self._args_dict)
                    self._log.info("init KafkaConsumer success")
            else:
                self._log.info('=== kafka producer kwargs is:{} ==='.format(self._args_dict))
                print('=== kafka producer kwargs is:{} ==='.format(self._args_dict))
                real_type = 'producer'
                self.client__ = KafkaProducer(**self._args_dict)
                self._log.info("init KafkaProducer success")
        except Exception as e:
            count += 1
            self._log.error('The {} times init_kafka error: {}\t{}'.format(count, str(e), traceback.format_exc()))
            time.sleep(self._retry_sleep_time)
            self._reconnect(count)

    # ------------------- 下列方法是额外封装的，大家可以自己选择性调用 ----------------
    def close(self, timeout=10, info=''):
        self._log.info('{} {} do  close'.format(info, self.singleton_sign))
        try:
            if getattr(self, "client__", None) is not None:
                if self._init_type == "consumer":
                    self.client__.close()
                else:
                    self.client__.close(timeout=timeout)
                self.client__ = None
        except:
            self._log.error(traceback.format_exc())

    # -------------- consumer ---------------
    # @kafka_type_check(init_type='consumer', real_type=real_type)
    def assign(self, partition):
        self._partition = partition
        self._reconnect()

    set_partition = assign

    # @kafka_type_check(init_type='consumer', real_type=real_type)
    def get_position(self, partition=None):
        if self._partition is None and partition is None:
            return None
        partition = self._partition or partition
        return self.client__.position(TopicPartition(self._topic, partition))

    # @kafka_type_check(init_type='consumer', real_type=real_type)    # todo 这个没有生效，因为装饰器，初期就被载入了？使用字典，也没有用。
    def get_partitions(self, topic=None):
        # print("real_type:{}".format(real_type))
        if topic and topic != self._topic:
            self._topic = topic
            self._reconnect()
        self.client__.topics()
        partitions_list = self.client__.partitions_for_topic(self._topic)
        return partitions_list

    get_partitions_list = get_partitions

    # @kafka_type_check(real_type=real_type)
    def get_messages(self, timeout_ms=5000, max_records=1000, value_type='tuple', decode=False):
        messages = self.client__.poll(timeout_ms=timeout_ms, max_records=max_records)
        if not messages:
            return []
        messages = reduce(lambda x, y: x + y, list(messages.values()))
        if value_type == 'dict':
            data = [{"partition": m.partition, "offset": m.offset, "value": m.value} for m in messages]
        else:
            data = [(m.partition, m.offset, m.value) for m in messages]
        if decode:
            data = decoder(data)
        return data

    """todo 这个方法目前有点问题，不要使用！！！"""
    @property
    # @kafka_type_check(real_type=real_type)
    def _messages(self):
        for m in self.client__:
            yield m if not self._hide_detail else (m.partition, m.offset, m.value)

    # @kafka_type_check(real_type=real_type)
    def commit(self, offsets=None):
        if self._enable_auto_commit:
            raise ValueError('can not commit ,auto commit set.')
        if not self._group_id:
            raise ValueError('must have group_id')
        if offsets:
            if self._partition is None:
                raise ValueError('commit offsets must have certain partition.')
            meta = self.client__.partitions_for_topic(self._topic)
            commit_offsets = dict()
            commit_offsets[TopicPartition(self._topic, self._partition)] = OffsetAndMetadata(offsets, meta)
            offsets = commit_offsets
        self.client__.commit(offsets=offsets)
        return True

    # -------------- producer ---------------
    # @kafka_type_check(init_type='producer', real_type=real_type)
    def flush(self, timeout=None):
        return self.client__.flush(timeout)

    # @kafka_type_check(init_type='producer', real_type=real_type)
    def err_callback(self, **kwargs):
        self._log.error("Send Data to kafka broker Error {}, {}".format(kwargs))

    def _send_action(self, value=None, key=None, partition=None, topic=None):
        topic = topic or self._topic
        partition = partition or self._partition
        if isinstance(value, str):
            value = value.encode('utf-8')
        elif isinstance(value, (dict, list, tuple)):
            value = json.dumps(value).encode('utf-8')
        elif isinstance(value, bytes):
            pass
        else:
            self._log.error("data type not supported.type: %s" % type(value))
        kwargs = {"value": value}
        if key:
            kwargs["key"] = key
        if partition:
            kwargs["partition"] = partition
        produce_future = self.client__.send(topic, **kwargs)
        produce_future.add_errback(self.err_callback, message=value)

    # @kafka_type_check(init_type='producer', real_type=real_type)
    def send(self, value: (bytes, str, dict, list, tuple), key=None, partition=None, topic=None, auto_flush=True):
        """
        发送内容，默认自动提交。value 可以是 字符串，字典
        """
        auto_flush = auto_flush or self._auto_flush
        self._send_action(value, key, partition, topic)
        if auto_flush:
            self.flush()
        return True

    def send_many(self, data: iter, partition=None, topic=None, auto_flush=True):
        """一次性发送很多数据"""
        if isinstance(data, (list, set)):
            for each in data:
                self._send_action(each, partition)
        elif isinstance(data, dict):
            for key, value in data.items():
                self._send_action(value, key, partition, topic)
        else:
            self._log.error("data type not supported.type: %s" % type(data))
        if auto_flush:
            self.flush()
        return True
