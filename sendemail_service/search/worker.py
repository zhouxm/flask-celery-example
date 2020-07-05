import random
import time

from . import cel


@cel.task(bind=True)
def send_async_email(self, email_data):
    """Background task to send an email with Flask-Mail."""
    # print(f"=========>send_async_email:{email_data}")

    pass


@cel.task(bind=True)
def long_task(self):
    """Background task that runs a long function with progress reports."""
    pass
