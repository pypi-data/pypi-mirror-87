import logging
import json
import uuid
import cachetools
import sys
import requests
from copy import deepcopy
from traceback import format_exc


logger = logging.getLogger("requests")


@cachetools.cached(cache=cachetools.TTLCache(maxsize=1024, ttl=6 * 60))
def requester(method, url, data):
    data = json.loads(data)
    response = getattr(requests, method)(url, **data)
    return response


class External(object):

    headers = {}

    @classmethod
    def get(cls, url, **kwargs):
        return cls.request("get", url, **kwargs)

    @classmethod
    def post(cls, url, **kwargs):
        return cls.request("post", url, **kwargs)

    @classmethod
    def request(cls, method, url, cache=False, **kwargs):
        # kwargs.update(verify=False)  # 不校验ssl证书
        kwargs.setdefault('headers', cls.headers)
        kwForLog = deepcopy(kwargs)
        kwForLog.get("files") and kwForLog.update(files="upload a file")
        for _ in range(3):
            try:
                if cache:
                    response = result = requester(method, url, json.dumps(kwargs))
                else:
                    response = result = getattr(requests, method)(
                        url, verify=False, **kwargs
                    )
            except requests.exceptions.Timeout:
                cls.errorLogger(method, url, reason="Timeout")
                continue
            except requests.exceptions.RequestException:
                cls.errorLogger(method, url, **kwForLog)
                return {}
            else:
                break
        else:
            return {}

        try:
            result = result.json()
        except Exception as e:
            cls.errorLogger(method, url, response=response, **kwForLog)
            return {}
        if result is None or result == b"":
            result = {}  # 对产品返回为'null'做处理
        cls.successLogger(method, url, response, **kwForLog)
        return result

    @staticmethod
    def successLogger(method, url, response, **kwargs):
        logger.info(f"{'Request done':-^70}")
        logger.info(f"{method.upper()} {url}")
        logger.info(f"kwargs: {kwargs}")
        logger.info(f"Response: {response.status_code} {response.text}")
        logger.info(f"{'-' * 70}\n\n\n")

    @staticmethod
    def errorLogger(method, url, reason=None, response=None, **kwargs):
        logger.info("Request:")
        logger.info(f"{method.upper()} {url}")
        logger.info(f"kwargs: {kwargs}")
        if reason is not None:
            logger.error(f"error reason: {reason}")
        if response is not None:
            resp = (
                response.content
                if not isinstance(response, (list, dict, str))
                else repr(response)
            )
            logger.error(f"Response:{response.status_code} {resp}")
            logger.error(f"Json error: {format_exc()}")
        else:
            logger.error(f"Request error: {format_exc()}")


class Requests(object):

    headers = {'Content-Type': 'application/json; charset=utf-8'}

    def __init__(self):
        self.setup()

    def setup(self):
        pass

    def get(self, url, **kwargs):
        return self.request('get', url, **kwargs)

    def post(self, url, **kwargs):
        return self.request('post', url, **kwargs)

    def request(self, method, url, cache=False, **kwargs):
        if cache:
            _kwargs = json.dumps(kwargs)
            return self._cacheRequest(method, url, _kwargs)
        else:
            return self._request(method, url, **kwargs)

    @cachetools.cached(cache=cachetools.TTLCache(maxsize=1024, ttl=6 * 60))
    def _cacheRequest(self, method, url, kwargs):
        kwargs = json.loads(kwargs)
        return self._request(method, url, **kwargs)

    def _request(self, method, url, **kwargs):
        kwargs.setdefault("headers", self.headers)
        jobId = uuid.uuid4().hex[:6]
        msg = f"Request[{jobId}] start."
        logger.info(f"{msg:-^70}")
        logger.info(f"{method.upper()} {url}")
        logger.info(f"kwargs: {kwargs}")
        try:
            response = requests.request(method, url, **kwargs)
            logger.info(
                f"Request succeed! Status code: {response.status_code}"
            )
            if kwargs.get("stream", False):
                logger.info("Content: Received a streaming response.")
            else:
                if sys.getsizeof(response.content) / 1024 > 100:
                    logger.info("Content: Received a large size content.")
                else:
                    logger.info(f"Content: {response.content}")
        except Exception:
            logger.error("Request failed!")
            logger.error(format_exc())
            response = None
        msg = f"Request[{jobId}] done."
        logger.info(f"{msg:-^70}\n\n\n")
        return response
