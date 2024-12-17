from celery import Celery
from kombu import Exchange, Queue
import time

# Celery configuration for RabbitMQ
CELERY_BROKER_URL = 'amqp://localhost'  # RabbitMQ broker
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'     # redis result backend

# Initialize Celery app
celery_app = Celery('task_scheduler', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)

# Declare the queue with priority support
celery_app.conf.task_queues = (
    Queue('default', routing_key='default', queue_arguments={'x-max-priority': 10}, durable=True),
)

# Default Celery queue and routing configurations
celery_app.conf.task_default_queue = 'default'
celery_app.conf.task_default_exchange = 'default'
celery_app.conf.task_default_routing_key = 'default'

# Retry connecting to RabbitMQ if it's down on startup
celery_app.conf.broker_connection_retry_on_startup = True

# Results expire after 1 hour
celery_app.conf.result_expires = 3600

@celery_app.task(bind=True, acks_late=True)
def process_task(self, task_id, task_data, priority, timestamp):
    """
    Process a task with the given task ID, data, priority, and timestamp.
    """
    print(f"Processing task {task_id}: {task_data} (Priority: {priority}, Submitted at: {timestamp})")
    time.sleep(5)  # Simulate a delay
    result = f"Task {task_id} processed successfully (Priority: {priority}, Submitted at: {timestamp})."
    print(result)
    return result
