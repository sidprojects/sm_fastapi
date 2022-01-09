from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .config import settings

SQLALCHEMY_DB_URL = f'postgresql://{settings.db_username}:{settings.db_passwd}@{settings.db_hostname}:{settings.db_port}/{settings.db_name}'

engine = create_engine(SQLALCHEMY_DB_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        

# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='fastapi_db', user='postgres',
#                                 password='sabc1234', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connection succesfull!")
#         break
        
#     except Exception as error:
#         print("Connection to Database failed")
#         print(f"Error: {error}")
#         time.sleep(5)