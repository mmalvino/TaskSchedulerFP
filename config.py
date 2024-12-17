class Config:
    """
    Configuration settings for the application.
    """
    DEBUG = True
    CELERY_BROKER_URL = 'amqp://localhost'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
