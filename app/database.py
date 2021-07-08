import os
import databases
import sqlalchemy

from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.environ.get("DB_NAME", "polygon")
DB_USER = os.environ.get("DB_USER", "postgres")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "postgres")
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_PORT = os.environ.get("DB_PORT", "5432")

DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

db = databases.Database(DB_URL)
metadata = sqlalchemy.MetaData()

engine = sqlalchemy.create_engine(DB_URL)
metadata.create_all(engine)
