from src.user.dtos import UserSchema, LoginSchema
from sqlalchemy.orm import Session
from src.user.models import UserModel
from fastapi import HTTPException, status, Request
from pwdlib import PasswordHash
from datetime import datetime, timedelta
import jwt
from src.utils.settings import settings
from jwt.exceptions import InvalidTokenError
from src.utils.mail import send_email

### !. Password Hashing
password_hash = PasswordHash.recommended()

def get_password_hash(password):
    return password_hash.hash(password)

def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)

async def register(body:UserSchema, db:Session):

    ### !. 1 Username Validation
    is_user = db.query(UserModel).filter(UserModel.username == body.username).first()
    if is_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")
    
    ### !. 2 Email Validation
    is_user = db.query(UserModel).filter(UserModel.email == body.email).first()
    if is_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email Address already exists")
    
    ### !. 3 Password Validation
    hash_password = get_password_hash(body.hash_password)
    
    new_user = UserModel(
        name = body.name,
        username = body.username,
        hash_password = hash_password,
        email = body.email
    )
  
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    ### !. send email
    await send_email([new_user.email])
    
    return new_user

def user_login(body:LoginSchema, db:Session):
    ### ! 1. Username Validation
    user = db.query(UserModel).filter(UserModel.username == body.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You Entered Wrong Username !")
    
    if not verify_password(body.hash_password, user.hash_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You Entered Wrong password !")
        
    exp_time=datetime.now() + timedelta(minutes=settings.EXP_TIME)
    
    token = jwt.encode({"_id":user.id, "exp": exp_time.timestamp()},settings.SECRETE_KEY, settings.ALGORITHM)
    return {"token":token}

### ! Token send

def is_authenticate(request:Request, db:Session):
    try:
        token = request.headers.get("authorization")
        if not token:
            raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail="You are unauthorized.")
        toten = token.split(" ")[-1]
        
        data = jwt.decode(toten, settings.SECRETE_KEY, settings.ALGORITHM)
        user_id = data.get("_id")
        
        user = db.query(UserModel).filter(UserModel.id == user_id).first()
        if not user:
            raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail="You are unauthorized.")

        return user
    except InvalidTokenError:
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail="You are unauthorized.")