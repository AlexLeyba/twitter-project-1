from celery import shared_task

@shared_task
def create_ran():
    total = 50
    return total