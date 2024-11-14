from celery import shared_task
import time


@shared_task
def test_celery():
    time.sleep(5)
    return "Celery is Working"



@shared_task
def add(x, y):
    return x + y
