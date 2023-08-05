import unittest
from unittest import mock

from requests import Response

from hyperstools.configcenter import getConfigCenter


class TestConfigCenter(unittest.TestCase):
    @mock.patch("requests.get")
    def test_getconfigcenter(self, mock):
        response = Response
        content = """{
    "name": "test",
    "profiles": ["default"],
    "label": null,
    "version": null,
    "state": null,
    "propertySources": [{
        "name": "https://git.hypers.com/server-java/config-repo.git/hma_spring_cloud/hma-default.yml",
        "source": {
            "mysql.username": "mysqlUsermysql",
            "mysql.url.scheme": "https"
        }
    }, {
        "name": "https://git.hypers.com/server-java/config-repo.git/hma_spring_cloud/hma.yml",
        "source": {
            "redis.username": "redisUsername"
        }
    }]
    }""".encode(
            "utf8"
        )
        response.content = content
        mock.return_value = response()
        configcenter = getConfigCenter(
            "http://127.0.0.1", "test", "default", "python", "username", "password"
        )
        self.assertEqual(configcenter.mysql.username, "mysqlUsermysql")
        self.assertEqual(configcenter.mysql.url.scheme, "https")
        self.assertEqual(configcenter.redis.username, "redisUsername")
