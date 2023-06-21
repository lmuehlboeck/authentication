import os
from fastapi import FastAPI, status, HTTPException, Depends, Response, Request, Cookie
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta
from uuid import uuid4
from pydantic import ValidationError

from crud import *
from schemas import UserLogin, User
from database import SessionLocal, Base, engine

ACCESS_TOKEN_EXP_MIN = 5
REFRESH_TOKEN_EXP_MIN = 60 * 12
ALGORITHM = "HS256"

if "SECRET_KEY" not in os.environ:
    os.environ["SECRET_KEY"] = uuid4().hex
SECRET_KEY = os.environ["SECRET_KEY"]

Base.metadata.create_all(bind=engine, checkfirst=True)

app = FastAPI()

origins = ["http://localhost:8080", "http://localhost:1337", "https://auth.byleo.net"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_access_token(data: dict, exp_time_min: int) -> str:
    return jwt.encode(
        data | {"exp": datetime.utcnow() + timedelta(minutes=exp_time_min)},
        SECRET_KEY, ALGORITHM)
    
def verify_access_token(request: Request) -> User:
    access_token = request.headers.get("Authorization")
    if not access_token:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Authentication required!")
    try:
        payload = jwt.decode(access_token, SECRET_KEY, ALGORITHM)
        user = User(**payload)
        if 0 >= user.role >= 2:
            raise HTTPException(status.HTTP_403_FORBIDDEN, "User not authorized to access this resource!")
        return user
    except (JWTError, ValidationError):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid access token!")

@app.post("/api/user", status_code=status.HTTP_201_CREATED)
def register(credentials: UserLogin, db: Session = Depends(get_db)):
    if 2 <= len(credentials.username) >= 32 or len(credentials.password) < 6:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid built username or password!")
    if get_user_by_username(db, credentials.username):
        raise HTTPException(status.HTTP_409_CONFLICT, "Username already existing!")
    create_user(db, credentials)
    return {"message": "User created successfully"}

@app.post("/api/session")
def login(credentials: UserLogin, response: Response, db: Session = Depends(get_db)):
    user = verify_user(db, credentials)
    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid username or password!")
    if user.role < 0:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "User blocked!")
    access_token = create_access_token(dict(user), ACCESS_TOKEN_EXP_MIN)
    refresh_token = create_refresh_token(db, user, REFRESH_TOKEN_EXP_MIN)
    response.set_cookie(key="refresh_token", value=refresh_token, httponly=True, samesite="None", secure=True, path="/api/session")
    return {"access_token": access_token}

@app.put("/api/session")
def refresh(refresh_token: str | None = Cookie(None), db: Session = Depends(get_db)):
    if not refresh_token:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Refresh token missing!")
    user = verify_refresh_token(db, refresh_token)
    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid refresh token!")
    if user.role < 0:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "User blocked!")
    return {"access_token": create_access_token(user.dict(), ACCESS_TOKEN_EXP_MIN)}

@app.delete("/api/session")
def logout(response: Response, refresh_token: str | None = Cookie(None), db: Session = Depends(get_db)):
    if not refresh_token:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Refresh token missing!")
    delete_refresh_token(db, refresh_token)
    response.set_cookie(key="refresh_token", value="", httponly=True, samesite="None", secure=True, path="/api/session")
    return {"message": "Logged out successfully"}

@app.get("/api/user")
def check(user: User = Depends(verify_access_token)) -> User:
    return user

@app.delete("/api/user")
def delete_user(response: Response, user: User = Depends(verify_access_token), db: Session = Depends(get_db)):
    delete_user(db, user)
    response.set_cookie(key="refresh_token", value="", httponly=True, samesite="None", secure=True, path="/api/session")
    delete_refresh_tokens_by_user(db, user)
    return {"message": "User deleted successfully"}