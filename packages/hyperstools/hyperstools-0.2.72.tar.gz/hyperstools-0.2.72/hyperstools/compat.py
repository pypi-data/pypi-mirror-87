# encoding: utf-8

import json
import os

defaultMq = {
    "host": "127.0.0.1",
    "port": "5672",
    "user": "admin",
    "password": "admin",
    "vhost": "/",
    "exchange": "test",
    "queue": "test",
    "routing_key": "test",
}
ssl_flag = False

def _close_old_connections(*args, **kwargs):
    pass


try:
    import django

    settings = django.conf.settings
    defaultMq = settings.RABBITMQ
    ssl_flag = defaultMq.get("ssl", False)
    close_old_connections = django.db.close_old_connections
except Exception:
    close_old_connections = _close_old_connections

if os.environ.get("RABBITMQ"):
    defaultMq = json.loads(os.environ["RABBITMQ"])
