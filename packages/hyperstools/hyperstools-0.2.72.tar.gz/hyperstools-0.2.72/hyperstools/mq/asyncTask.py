# encoding: utf-8
import inspect
import uuid
import logging
from traceback import format_exc
from django.conf import settings
from functools import wraps
from importlib import import_module
from .lib import Queue

logger = logging.getLogger("tools")


_queue = getattr(settings, 'ASYNC_TASK_QUEUE', 'async.task')
identify = {'queue': _queue}
_container = {}


def listener(data):
    """
    异步任务的回调函数
    其中参数经过pickle.loads
    """
    callback = _container[data["callback"]]
    args = data.get("args", [])
    kwargs = data.get("kwargs", {})
    try:
        callback(*args, **kwargs)
    except Exception:
        logger.error(format_exc())


listen = Queue(identify, logger=logger)(listener)


def register(task):
    """
    注册异步任务的装饰器
    直接调用回调函数时会发送消息到队列aurora.async.task
    跟正常调用方法无区别
    其中会把函数的参数用pickle.dumps， 然后发送消息

    使用方法

    @register
    def mycallback(model, queryset):
        pass

    mycallback(model, queryset)
    """
    _container[task.__name__] = task

    def inner(*args, **kwargs):
        taskId = uuid.uuid4().hex
        if 'taskId' in inspect.getfullargspec(task).args:
            kwargs.update(taskId=taskId)
        with Queue(identify, logger=logger) as queue:
            message = {"callback": task.__name__, "args": args, "kwargs": kwargs}
            queue.publish(message, encoder="pickle")
        return taskId

    return inner


def register2(queue=_queue):
    """
    注册异步任务的装饰器,
    默认队列为 settings.ASYNC_TASK_QUEUE, 如未定义, 则为 async.task
    直接调用回调函数时会发送消息到队列指定的消息队列
    跟正常调用方法无区别
    其中会把函数的参数用pickle.dumps， 然后发送消息

    """
    def decorator(task):
        @wraps(task)
        def inner(*args, callback=False, **kwargs):
            if callback:
                return task(*args, **kwargs)
            taskId = uuid.uuid4().hex
            if 'taskId' in inspect.getfullargspec(task).args:
                kwargs.update(taskId=taskId)
            _identify = {'queue': queue}
            with Queue(_identify, logger=logger) as q:
                _callback = f"{task.__module__}.{task.__qualname__}"
                message = {"callback": _callback, "args": args, "kwargs": kwargs}
                q.publish(message, encoder="pickle")
            return taskId
        return inner
    return decorator


class Listener:
    def __init__(self, queue=_queue):
        self.queue = queue

    @staticmethod
    def callback(msg):
        _callback = msg["callback"].split(".")
        for step in range(1, len(_callback)):
            path = ".".join(_callback[:-step])
            try:
                module = import_module(path)
            except ModuleNotFoundError:
                continue
            else:
                obj = module
                for o in _callback[-step:]:
                    obj = getattr(obj, o)
                break
        args, kwargs = msg["args"], msg["kwargs"]
        if inspect.ismethod(obj):  # 类方法和成员方法需要去掉隐式传递的参数
            args = list(args)
            args.pop(0)
        obj(*args, callback=True, **kwargs)

    def listen(self):
        _identify = {'queue': self.queue}
        Queue(_identify, logger).listen(self.callback)


listen2 = Listener().listen

