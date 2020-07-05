# ----init.py----
from celery import Celery

def make_celery(app):
    """创建celery"""

    cele = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'], backend=app.config['CELERY_RESULT_BACKEND'])
    cele.conf.update(app.config)
    TaskBase = cele.Task

    # 配置Flask上下文
    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    cele.Task = ContextTask

    return cele
