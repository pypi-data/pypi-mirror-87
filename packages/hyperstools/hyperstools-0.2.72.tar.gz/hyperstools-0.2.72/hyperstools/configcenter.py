"""
获取配置中心
调用getConfigCenter方法 传入参数: 配置中心url, 应用名,环境名, HTTP Basic Auth用户名,HTTP Basic Auth密码

example:
configcenter = getConfigCenter('http:www.configcenter.com','hfa','test','admin','password')
mysqlUrl = configcenter.mysql.url
redis = configcenter.redis

如果是 git仓库的非master分支, 那么请求参数需要加入branch名,
example:
configcenter = getConfigCenter('http:www.configcenter.com','hfa','test','admin','password', 'develop')
mysqlUrl = configcenter.mysql.url
redis = configcenter.redis

"""

import requests
from requests.auth import HTTPBasicAuth
from urllib.parse import urljoin


class ConfigFactory(object):
    """配置中心, 实现配置的链式调用"""

    def __init__(self, map):
        self.map = map

    def __getattr__(self, item):
        child = self.map.get(item, None)
        if not child:
            raise KeyError(f"配置中心找不到: {item}, 请检查")
        if isinstance(child, dict):
            map = ConfigFactory(child)
            return map
        else:
            return child

    def __str__(self):
        return str(self.map)

    def __repr__(self):
        return str(self.map)


class ConfigHandle(object):
    """请求java的config-server, 并且格式化返回的response"""

    def __init__(self, url, application, profile, username, password, branch):
        self.config = requestConfigServer(url, application, profile, username, password, branch)

    def getConfig(self):
        config = self.formatConfit(self.config)
        return config

    def formatConfit(self, config):
        """将response格式化成ConfigMapping需要的格式, 实现链式调用"""
        result = dict()
        for key, value in config.items():
            keyList = key.split(".")
            keyCount = len(keyList)
            if keyCount == 1:
                result[key] = value
            else:
                for i in range(keyCount):
                    if i == 0:
                        tmp = result.setdefault(keyList[i], {})
                    elif i < (keyCount - 1):
                        tmp = tmp.setdefault(keyList[i], {})
                    else:
                        tmp[keyList[i]] = value
        return result

    def getAllConfig(self):
        """获取所有的配置"""
        return self.config


def requestConfigServer(url, application, profile, username, password, branch):
    """
    请求配置中心 获取项目配置
    :param url: git仓库地址
    :param application:  项目名
    :param profile: 环境名
    :param username: HTTP Basic Auth 认证的用户名
    :param password: HTTP Basic Auth 认证的密码
    :return: 各项配置, 数据格式为字典
    """
    if branch:
        path = f"{application}/{profile}/{branch}"
    else:
        path = f"{application}/{profile}"
    response = requests.get(
        urljoin(url, path),
        auth=HTTPBasicAuth(username, password),
        timeout=60,
        headers={"User-Agent":  "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5"}
    )
    if response.status_code == 200:
        response = response.json()
    else:
        raise Exception("访问配置中心失败")
    propertySources = response.get("propertySources", [])
    config = mergeConfig(propertySources)
    return config


def mergeConfig(propertySources):
    """将property_sources的各项配置整合到一个字典里"""
    config = dict()
    for property in propertySources:
        source = property.get("source", {})
        for key, value in source.items():
            config[key] = value
    return config


def getConfigCenter(
    url=None, application=None, profile=None,  username=None, password=None, branch=None,
):
    """
   获取配置中心类
   :param url: git仓库地址
   :param application:  项目名
   :param profile: 环境名
   :param username: HTTP Basic Auth 认证的用户名
   :param password: HTTP Basic Auth 认证的密码
   :param branch :仓库分支名, 默认None
   :return: ConfigCenter 实例
   """
    configHandler = ConfigHandle(url, application, profile, username, password, branch)
    config = ConfigFactory(configHandler.getConfig())
    return config
