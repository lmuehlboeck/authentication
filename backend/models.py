from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(32), unique=True)
    password = Column(String(255))
    role = Column(Integer, default=0)

    refresh_tokens = relationship("RefreshToken", back_populates="user", passive_deletes=True)

class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    token = Column(String(255), primary_key=True)
    expiration_time = Column(DateTime)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

    user = relationship("User", back_populates="refresh_tokens")
