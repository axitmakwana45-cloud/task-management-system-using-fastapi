from fastapi import APIRouter,Depends,status,Request,Header
from sqlalchemy.orm import Session
from src.user.dtos import userschema,userresponceschema,loginschema
from src.utils.db import get_db
from src.user import controller

user_router = APIRouter(prefix="/user")


@user_router.post("/register",response_model=userresponceschema,status_code=status.HTTP_201_CREATED)
def register(body : userschema, db = Depends(get_db)):
    return controller.register(body,db) 

@user_router.post("/login",status_code=status.HTTP_200_OK)
def login_user(body : loginschema,db = Depends(get_db)):
    return controller.login_user(body ,db)

@user_router.get("/is_auth",response_model=userresponceschema, status_code=status.HTTP_200_OK)
def is_auth(
    request : Request,
    db: Session = Depends(get_db)
):
    return controller.is_authenticated(request, db)