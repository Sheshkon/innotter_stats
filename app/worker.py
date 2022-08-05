from celery import Celery
from app.config import settings


app = Celery(
    'worker',
    broker=f'amqp://{settings.RABBITMQ_DEFAULT_USER}:{settings.RABBITMQ_DEFAULT_PASS}@{settings.RABBITMQ_HOSTNAME}//',
    result_backend=f'dynamodb://@{settings.AWS_DEFAULT_REGION}',
    dynamodb_endpoint_url=f'{settings.LOCALSTACK_ENDPOINT_URL}',
    result_persistent=False,
    include=['app.tasks']
)

app.conf.setdefault('task_default_queue', 'microservice_stats')
app.conf.update(task_track_started=True)
