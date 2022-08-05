import os

from pydantic import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    APP_NAME: str = os.environ.get("APP_NAME")
    SECRET_KEY: str = os.environ.get("SECRET_KEY")
    AWS_DEFAULT_REGION: str = os.environ.get("AWS_DEFAULT_REGION")
    AWS_ACCESS_KEY_ID: str = os.environ.get("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY: str = os.environ.get("AWS_SECRET_ACCESS_KEY")
    LOCALSTACK_ENDPOINT_URL: str = os.environ.get("LOCALSTACK_ENDPOINT_URL")
    AWS_PROFILE: str = os.environ.get('AWS_PROFILE')
    INNOTTER_STATS_TABLE: str = os.environ.get('INNOTTER_STATS_TABLE')
    STATS_TABLE: str = os.environ.get('STATS_TABLE')
    RABBITMQ_DEFAULT_USER: str = os.environ.get('RABBITMQ_DEFAULT_USER')
    RABBITMQ_DEFAULT_PASS: str = os.environ.get('RABBITMQ_DEFAULT_PASS')
    RABBITMQ_HOSTNAME: str = os.environ.get('RABBITMQ_HOSTNAME')


settings = Settings()
