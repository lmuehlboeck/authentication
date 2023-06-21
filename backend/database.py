from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import text

DATABASE_URL = "mysql+pymysql://root:password@database/mysql"

engine = create_engine(
    DATABASE_URL
)

SessionLocal = sessionmaker(autoflush=False, bind=engine)

SessionLocal().execute(text("CREATE DATABASE IF NOT EXISTS authentication"))
SessionLocal().execute(text("USE authentication"))

Base = declarative_base()