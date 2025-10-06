from jose import JWTError, jwt
from passlib.context import CryptContext
from database import get_db
import datetime
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from models import Users

get_db()

secret_key = "newecomm123"
password_crypt = CryptContext(schemes=["bcrypt"])

oauth_scheme = OAuth2PasswordBearer(tokenUrl="users/login")



def hash_password(user_password: str):
    return password_crypt.hash(user_password)

def verify_password(user_password, hashed_password):
    return password_crypt.verify(user_password, hashed_password)

def create_new_token(user_data: dict):
    user_data_copy = user_data.copy()
    exp = datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=30)
    user_data_copy.update({"exp": exp})
    return jwt.encode(user_data_copy, secret_key, algorithm="HS256")

def get_current_user(token: str = Depends(oauth_scheme), db: Session = Depends(get_db)):
    authentication_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could Not Validate Credentials",
        headers={"WWW-Authenticate": "Bearer"})
    try:
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        username: str = payload.get("username")
        if username is None:
            raise authentication_exception
        user = db.query(Users).filter(Users.username == username).first()
        if user is None:
            raise authentication_exception
        return user
    except JWTError:
        raise authentication_exception

def admin_only(user: Users = Depends(get_current_user)):
    if user.user_role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin Only")
    return user
    









