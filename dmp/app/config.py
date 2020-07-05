import os


class Config(object):
    """项目配置 (基类)"""

    # 根目录
    BASEDIR = os.path.abspath(os.path.dirname(__file__))

    # mysql
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True  # 请求结束之后进行数据自动提交
    SQLALCHEMY_ECHO = False  # 查看原始sql语句

    # redis
    REDIS_HOST = os.environ.get('REDIS_HOST') or "100.69.149.205"
    REDIS_PORT = os.environ.get('REDIS_PORT') or 6379  # 6380
    REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD') or 'm!N0BII3k'
    REDIS_NUM = os.environ.get('REDIS_NUM') or 1  # cache

    # celery
    # CELERY_URL = 'redis://:password@ip/port/db'  # 工人:password@ip/port/db
    CELERY_BROKER_NUM = os.environ.get('CELERY_BROKER_NUM') or 2  # worker
    CELERY_RESULT_NUM = os.environ.get('CELERY_RESULT_NUM') or 3  # result
    CELERY_BROKER_URL =     f'redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{CELERY_BROKER_NUM}'
    CELERY_RESULT_BACKEND = f'redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{CELERY_RESULT_NUM}'
    CELERY_TIMEZONE = 'Asia/Shanghai'  # 时区
