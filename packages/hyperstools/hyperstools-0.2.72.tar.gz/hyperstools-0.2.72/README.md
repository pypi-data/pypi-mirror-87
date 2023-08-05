# 说明
本库封装了S3,Rabbitmq,Apscheduler,ssh, sftp, 以及常用的函数


## S3
使用boto3封装S3,
假设在settings已经配置好settings.S3

    {"host": "s3.hypers.com.cn", "port": 80, "access_key": "OPL5N7K242QFEA4SL0PB", "secret_key": "VsSSacotwZCCcvTOqMApPaEAS1JN2WDTD7dVKJPe", "bucket": "aurora"}
使用方法如下

获取某个key的url

    S3(key='test').url

下载S3文件到本地文件(tmp)

    S3().download('test', 'tmp')

获取某个目录下的子目录和文件(dir)

    S3().listdir(dir)

判断某个文件是否存在(name)

    S3().exists(name)

删除文件(name)

    S3().delete(name)

移动文件(key, name)

    S3().move(key, name)

复制文件(key, name)

    S3().copy(key, name)

下载S3文件到BytesIO对象

    bio = S3().download('test')

上传本地文件(test)到 S3路径(tmp)

    S3().upload('test', 'tmp')

上传本地文件BytesIO文件(bio)到 S3路径(tmp)

    bio = io.BytesIO()
    bio.write(b'test')
    bio.seek(0)
    S3().upload(bio, 'tmp')

设置S3文件('tmp')的权限，其中public-read为公网匿名用户可读

    S3().putACL('tmp', 'public-read')

## Rabbitmq
使用asyncio adapter封装rabbitmq的consumer,使用rabbitmq实现异步任务
假设在settings已经配置好settings.RABBITMQ, 如果没有配置，则在Queue实例化时吧配置传进去

    {"host": "10.123.99.99",
    "port": 5672,
    "vhost": "/kk",
    "user": "admin",
    "password": "admin",
    "queue": "aurora-test.back2front.calc.result.request.queue",
    }


### Consumer
默认在callback函数调用完之后发送ack信号

    @Queue()
    def listen(body: dict):
        print(body)

如果要在callback函数调用前发送ack信号

    @Queue(ack='first')
    def listen(body: dict):
        print(body)

### Publisher

    Queue().publish({'a': 'b'})

### 异步任务

    from hyperstools.mq.asyncTasker
    @asyncTasker.register
    def mycallback(model, queryset):
        pass

### django自定义查询器
    from hyperstools.django_extensions.lookups import NoCase

    NoCase.register()
