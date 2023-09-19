from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from .config import Settings

settings = Settings()
database = settings.database
ipaddress = settings.host
db_username = settings.db_username
password = settings.password
print(db_username)

SQLALCHEMY_DATABASE_URL = f"postgresql://{db_username}:{password}@{ipaddress}/{database}"
print(SQLALCHEMY_DATABASE_URL)
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base() 

"""SQL_Alchemy dependency"""
def get_db():
    db = SessionLocal()
    try:
        yield db 
    finally:
        db.close()
