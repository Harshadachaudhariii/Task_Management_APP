from fastapi import APIRouter, status, Depends, Request
from sqlalchemy.orm import Session
from src.user import controller
from src.user.dtos import UserSchema, UserResponseSchema, LoginSchema
from src.utils.db import get_db

user_routes = APIRouter(prefix="/user")

@user_routes.post("/register", response_model=UserResponseSchema,status_code=status.HTTP_201_CREATED)
async def register(body:UserSchema, db:Session =Depends(get_db)):
    return await controller.register(body, db)


@user_routes.post("/login", status_code=status.HTTP_200_OK)
def login(body: LoginSchema, db: Session = Depends(get_db)):
    return controller.user_login(body, db)

@user_routes.get("/is_auth",status_code=status.HTTP_200_OK, response_model=UserResponseSchema)
def is_auth(request:Request, db:Session=Depends(get_db)):
    return controller.is_authenticate(request, db)