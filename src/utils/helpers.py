
from fastapi import FastAPI,HTTPException,status,Request,Depends
from src.utils.settings import settings
from sqlalchemy.orm import Session
from jwt.exceptions import InvalidTokenError
import jwt
from src.user.models import Usermodel
from src.utils.db import get_db

def is_authenticated(request : Request, db: Session = Depends(get_db)):
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
        