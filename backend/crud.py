from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import datetime, timedelta
from uuid import uuid4

import models, schemas

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user(db: Session, id: int) -> schemas.User | None:
    db_user = db.query(models.User).filter_by(id=id).first()
    if not db_user:
        return None
    return schemas.User(id=db_user.id, username=db_user.username, role=db_user.role)

def get_user_by_username(db: Session, username: str) -> schemas.User | None:
    db_user = db.query(models.User).filter_by(username=username).first()
    if not db_user:
        return None
    return schemas.User(id=db_user.id, username=db_user.username, role=db_user.role)

def create_user(db: Session, user: schemas.UserLogin):
    hashed_password = pwd_context.hash(user.password)
    db.add(models.User(username=user.username, password=hashed_password, role=user.role))
    db.commit()

def verify_user(db: Session, user: schemas.UserLogin) -> schemas.User | None:
    db_user = db.query(models.User).filter_by(username=user.username).first()
    if not db_user or not pwd_context.verify(user.password, db_user.password):
        return None
    else:
        return schemas.User(id=db_user.id, username=db_user.username, role=db_user.role)

def delete_user(db: Session, user: schemas.User):
    db.query(models.User).filter_by(id=user.id).delete()
    db.commit()


def create_refresh_token(db: Session, user: schemas.User, exp_time_min: int) -> str:
    db.query(models.RefreshToken).filter(models.RefreshToken.user_id == user.id and models.RefreshToken.expiration_date < datetime.utcnow()).delete()
    token = uuid4().hex
    db.add(models.RefreshToken(token=token, expiration_time=datetime.utcnow()+timedelta(minutes=exp_time_min), user_id=user.id))
    db.commit()
    return token

def verify_refresh_token(db: Session, token: str) -> models.User | None:
    db_refresh_token = db.query(models.RefreshToken).filter_by(token=token).first()
    if not db_refresh_token or db_refresh_token.expiration_time < datetime.utcnow():
        return None
    return schemas.User(id=db_refresh_token.user.id, username=db_refresh_token.user.username, role=db_refresh_token.user.role)

def delete_refresh_token(db: Session, token: str):
    db.query(models.RefreshToken).filter_by(token=token).delete()
    db.commit()

def delete_refresh_tokens_by_user(db: Session, user: schemas.User):
    db.query(models.RefreshToken).filter_by(user_id=user.id).delete()
    db.commit()