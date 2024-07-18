import uuid

from backend.task.celery import celery_app


@celery_app.task(name='task_demo_async')
def task_demo_async() -> str:
    uid = uuid.uuid4().hex
    print(f'Async task with {uid} success! *******************')
    return uid
