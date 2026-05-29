from fastapi import HTTPException,status,Request
from src.user.dtos import userschema,loginschema
from sqlalchemy.orm import Session
from src.user.models import Usermodel
from pwdlib import PasswordHash
from src.utils.settings import settings
from datetime import datetime,timedelta
import jwt
from jwt.exceptions import InvalidTokenError


password_hash = PasswordHash.recommended()
def get_password_hash(password):
    return password_hash.hash(password)


def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)


def register(body : userschema,db : Session):
    is_user = db.query(Usermodel).filter(Usermodel.username == body.username).first()

    if is_user:
        raise HTTPException(400,detail="user name is already exist..")
    
    is_user = db.query(Usermodel).filter(Usermodel.email == body.email).first()
    
    if is_user:
        raise HTTPException(400,detail="email is already exist..")
    
    hash_password = get_password_hash(body.password)

    new_user = Usermodel(
        name = body.name,
        username = body.username,
        hash_password = hash_password,
        email = body.email,
        
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def login_user(body : loginschema,db: Session):
    user = db.query(Usermodel).filter(Usermodel.username == body.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="username or password is wrong")

    if not verify_password(body.password,user.hash_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="username or password is wrong")

    exp_time = datetime.now() + timedelta(minutes=settings.EXP_TIME)
    token = jwt.encode({"_id" : user.id,'exp':exp_time.timestamp()},settings.SECRET_KEY,settings.ALGORITHM)
    return {"token" : token}


def is_authenticated(request : Request, db: Session):
    try:    
        token = request.headers.get("authorization")
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="you are unauthorized"
            )

        token = token.split(" ")[-1]

        
        data = jwt.decode(
            token,
            settings.SECRET_KEY,
            settings.ALGORITHM
        )

        user_id = data.get("_id")
        # decode time j khabar thay jase exp nu
        # exp_time = data.get("exp")

        # current_time = datetime.now().timestamp()
        
        # if current_time > exp_time:
        #     raise HTTPException(
        #         status_code=status.HTTP_401_UNAUTHORIZED,
        #         detail="you are unauthorized"
        #     )

        user = db.query(Usermodel).filter(Usermodel.id == user_id).first()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="user is invalid"
            )

        return user
    except InvalidTokenError:
         raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="you are unauthorized"
            )
        