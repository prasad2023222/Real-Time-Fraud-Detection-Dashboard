import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()  # loads .env

DB_URL = os.getenv("DB_URL")
if not DB_URL:
    raise RuntimeError("DB_URL is not set")

engine = create_engine(DB_URL, pool_pre_ping=True)