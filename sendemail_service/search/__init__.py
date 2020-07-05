from celery import Celery

# Initialize Celery
cel = Celery("sendemail", broker="redis://localhost:6379/1", backend="redis://localhost:6379/0", include=["search.worker"])
cel.conf.timezone = "Asia/Shanghai"
cel.conf.enable_utc = False
