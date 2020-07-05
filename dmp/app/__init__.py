import logging

from celery import Celery
import os

from flask import Flask

from app.config import Config


def create_app(config_name):
    logging.info(f"FLASK_ENV:{os.getenv('FLASK_ENV', '-------')}")
    logging.info(f"config_name:{config_name}")
    app = Flask(__name__)
    app.config.from_object(Config)
    return app


def make_celery(app):
    """创建celery"""

    cele = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'], backend=app.config['CELERY_RESULT_BACKEND'])
    cele.conf.update(app.config)
    # TaskBase = cele.Task
    #
    # # 配置Flask上下文
    # class ContextTask(TaskBase):
    #     abstract = True
    #
    #     def __call__(self, *args, **kwargs):
    #         with app.app_context():
    #             return TaskBase.__call__(self, *args, **kwargs)
    #
    # cele.Task = ContextTask

    return cele
