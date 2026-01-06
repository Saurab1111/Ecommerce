from celery import shared_task

@shared_task()
def create_order(data):
    print("Processing order:", data)