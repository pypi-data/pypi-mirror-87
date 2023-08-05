# encoding: utf-8
import json
import logging
import pickle
import urllib

from .consumer import Consumer, EventLoopConsumer
from .publisher import Publisher
from hyperstools import compat
import asyncio
import collections
import threading

LOGGER = logging.getLogger("tools")
defaultMq = compat.defaultMq


class Queue(object):
    def __init__(self, identify: dict, logger=None, loop=None, **kwargs):
        """初始化rabbitmq的认证信息
        如果identify不存在host、port等key时，则从settings.RABBITMQ中取默认值

        :identify: dict: 认证信息， 如 {'user': 'xxx', 'password': 'xxx', 'queue': 'xxx'}
        :returns: None

        """
        host = identify.get("host", defaultMq["host"])
        port = identify.get("port", defaultMq["port"])
        user = identify.get("user", defaultMq["user"])
        password = identify.get("password", defaultMq["password"])
        vhost = identify.get("vhost", defaultMq["vhost"])
        exchange = identify.get("exchange", identify["queue"])
        routing_key = identify.get("routing_key", identify["queue"])
        exchange_type = identify.get("exchange_type", "direct")
        heartbeat = identify.get('heartbeat', defaultMq.get('heartbeat', 60))
        vhost = urllib.parse.quote_plus(vhost)
        ssl = identify.get("ssl", defaultMq.get("ssl", False))
        self._logger = logger or LOGGER
        self._loop = loop
        heartbeat = heartbeat and f"?heartbeat={heartbeat}" or ""
        amqp = "amqps" if ssl else "amqp"
        url = f"{amqp}://{user}:{password}@{host}:{port}/{vhost}{heartbeat}"
        self._identify = {
            "url": url,
            "exchange": exchange,
            "routing_key": routing_key,
            "queue": identify["queue"],
            "exchange_type": exchange_type,
        }
        self._kwargs = kwargs

    def publish(self, message: dict, encoder: str = "json"):
        """发布消息的处理函数
        用法
        with Queue(settings.RABBITMQ) as queue:
            queue.publish({'a': 'b'})

        :message: dict: 消息体
        :returns: None

        """
        if encoder == "pickle":
            body = pickle.dumps(message)
        else:
            body = json.dumps(message, ensure_ascii=False)
        messages = [body]
        pub = Publisher(
            self._identify, messages, logger=self._logger, **self._kwargs
        ).run()

    def listen(self, callback):
        consumer = Consumer(
            self._identify, callback, logger=self._logger, **self._kwargs
        )
        consumer.run()

    def __call__(self, callback):
        """注册listen的回调函数
        在调用callback函数之前，会先尝试使用json.loads 解析消息
        然后尝试使用pickle.loads 解析消息，
        如果解析消息失败，则直接返回ack,
        解析成功后会调用
        close_old_connections, 再调用callback函数
        其中回调消息会经过异常处理

        用法

        @Queue(settings.RABBITMQ)
        def listen(body: dict):
            pass

        listen()

        :callback: 消费者的回调函数
        :returns: None

        """

        def inner():
            return self.listen(callback)

        return inner

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass


class EventLoop(object):
    """EventLoop
    控制多条mq监听队列的eventloop

    eg.
    a.py
    @EventLoopQueue(config1, name="default")
    def listen()

    b.py
    @EventLoopQueue(config2, name="default")
    def listen()

    c.py
    def main():
        eventloop = EventLoop(name="default")
        eventloop.run()

    """
    taskLoopMap = collections.defaultdict(list)

    def __init__(self, name="default", logger=None):
        self.name = name
        self.queues = EventLoopQueue.queueMap[name]
        self.tasks = []

        self.threadLoop = asyncio.new_event_loop()
        self.processThread = threading.Thread(target=self.process)

        self.eventLoop = asyncio.get_event_loop()
        self.mapping = self.taskLoopMap[self.name]
        self.logger = logger or LOGGER

    def run(self):
        self.processThread.start()
        for queue in self.queues:
            listen = queue()
            self.tasks.append(listen)
        self.eventLoop.run_until_complete(self._run())
        self.eventLoop.run_forever()

    async def _run(self):
        done, pending = await asyncio.wait(self.tasks)
        futures = []
        # 将任务动态加入子线程中的事件循环
        while True:
            while self.mapping:
                callback, data = self.mapping.pop(0)
                future = asyncio.run_coroutine_threadsafe(
                    callback(data), self.threadLoop
                )
                futures.append((future, data))
            futures = self.logExceptions(futures)
            await asyncio.sleep(0)

    def logExceptions(self, futures):
        """logExceptions
        更新任务列表并记录异常信息

        :param futures: [处理中的任务列表]
        :type futures: [list]
        :return: [更新后的任务列表]
        :rtype: [list]
        """
        _futures = []
        for future, data in futures:
            if future.done():
                ex = future.exception()
                if ex:
                    tb = ex.__traceback__
                    _data = f"\ndata:  {data}\n"
                    _error = "Traceback (most recent call last):\n" + "".join(
                        traceback.format_tb(tb)
                    )
                    self.logger.error(_data + _error)
                future.cancel()
            else:
                _futures.append((future, data))
        return _futures

    def process(self):
        asyncio.set_event_loop(self.threadLoop)
        self.threadLoop.run_forever()


class EventLoopQueue(Queue):
    queueMap = collections.defaultdict(list)

    def __call__(self, callback):
        listen = self.listen(callback)
        self.queueMap[self._loop].append(listen)

    def listen(self, callback):
        consumer = EventLoopConsumer(
            self._identify,
            callback,
            logger=self._logger,
            loop=self._loop,
            **self._kwargs,
        )
        return consumer.run
