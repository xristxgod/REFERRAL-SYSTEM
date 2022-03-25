import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.join(ROOT_DIR, "DB")

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://username:password@host/table_name")