from core import celery_app
import time


@celery_app.task
def some_hard_function():
    time.sleep(10)
    return 'Success'
