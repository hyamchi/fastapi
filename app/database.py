from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker 
from sqlalchemy.engine import URL
from sqlalchemy import create_engine
import pyodbc
import time
from .config import settings

connection_url = f"mssql://@{settings.database_servername}/{settings.database_name}?driver={settings.database_driver}"
engine = create_engine(connection_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# while True:
#     try:
#         conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server}; Server=LOCALHOST\SQLEXPRESS; Database=fastapi; Trusted_Connection=yes; cursor_factory=RealDictCursor')
#         cursor = conn.cursor()
#         print("Connected to the database")
#         break
#     except Exception as error:
#         print("was not successful")
#         print(error)
#         time.sleep(2)