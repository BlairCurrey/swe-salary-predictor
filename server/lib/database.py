from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

IS_DEV = os.environ.get("IS_DEV", 'False').lower() == 'true'
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
DB_NAME = os.environ.get("DB_NAME")
DB_HOST = os.environ.get("DB_HOST")
DB_SOCKET_DIR = os.environ.get("DB_SOCKET_DIR", "/cloudsql")
INSTANCE_CONNECTION_NAME = os.environ.get("INSTANCE_CONNECTION_NAME")

# https://cloud.google.com/sql/docs/postgres/connect-app-engine-standard#python
SQLALCHEMY_DATABASE_URI = (f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"
                          if IS_DEV else
                          f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@/{DB_NAME}?host={DB_SOCKET_DIR}/{INSTANCE_CONNECTION_NAME}/")

engine = create_engine(SQLALCHEMY_DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    except:
        db.close()
