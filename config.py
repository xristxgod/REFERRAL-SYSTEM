import os
import logging

logger = logging.getLogger(__name__)

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.join(ROOT_DIR, "file")

class Config:

    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://username:password@host/table_name")

    TB_TOKEN = os.getenv("TB_TOKEN", "")
    ADMIN_IDS = os.path.join(BASE_DIR, "ADMIN_IDS.json")

    RABBIT_MQ_URL = os.getenv("RABBIT_MQ_URL", "amqp://test:test@127.0.0.1/")
    QUEUE = os.getenv("QUEUE", "TEST_QUEUE")

    SENDER_EMAIL = os.getenv("SENDER_EMAIL", "test88tset@gmail.com")
    SENDER_PASSWORD = os.getenv("SENDER_PASSWORD", "test88tset")

