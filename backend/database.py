from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import text

DATABASE_URL = "mysql+pymysql://root:password@localhost/authentication"

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True, 
    pool_recycle=300
)

SessionLocal = sessionmaker(autoflush=False, bind=engine)

Base = declarative_base()